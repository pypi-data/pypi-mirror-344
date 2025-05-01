"""
ScmRun provides a high level analysis tool for simple climate model relevant data

It provides a simple interface for reading/writing, subsetting and visualising
model data. ScmRuns are able to hold multiple model runs which aids in analysis of
ensembles of model runs.
"""
from __future__ import annotations

import copy
import datetime as dt
import numbers
import os
import pathlib
import warnings
from logging import getLogger
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Literal,
    Mapping,
    Sequence,
    TypeVar,
    cast,
    overload,
)

import cftime  # type: ignore
import numpy as np
import numpy.testing as npt
import pandas as pd
import pandas.io.common
import pint
from dateutil import parser
from typing_extensions import Self

import scmdata.units

from ._base import OpsMixin
from ._typing import ApplyCallable, FilePath, MetadataType, MetadataValue
from ._xarray import inject_xarray_methods
from .errors import (
    DuplicateTimesError,
    MissingRequiredColumnError,
    NonUniqueMetadataError,
)
from .filters import (
    HIERARCHY_SEPARATOR,
    datetime_match,
    day_match,
    hour_match,
    month_match,
    pattern_match,
    years_match,
)
from .netcdf import inject_nc_methods
from .offsets import generate_range, to_offset
from .ops import inject_ops_methods
from .plotting import inject_plotting_methods
from .time import _TARGET_DTYPE, TimePoints, TimeseriesConverter
from .units import UnitConverter

_logger = getLogger(__name__)


GenericRun = TypeVar("GenericRun", bound="BaseScmRun")


if TYPE_CHECKING:
    from numpy.typing import NDArray
    from typing_extensions import Concatenate, ParamSpec

    from scmdata.groupby import RunGroupBy

    from .pyam_compat import LongDatetimeIamDataFrame

    P = ParamSpec("P")


def _read_file(  # pylint: disable=missing-return-doc
    filename: FilePath, required_cols: Sequence[str], *args: Any, **kwargs: Any
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare data to initialize :class:`ScmRun <scmdata.run.ScmRun>` from a file.

    Parameters
    ----------
    *args
        Passed to :func:`_read_pandas`.
    **kwargs
        Passed to :func:`_read_pandas`.

    Returns
    -------
    :class:`pandas.DataFrame`, :class:`pandas.DataFrame`
        First dataframe is the data. Second dataframe is metadata
    """
    _logger.info("Reading %s", filename)

    return _format_data(_read_pandas(str(filename), *args, **kwargs), required_cols)


def _read_pandas(
    fname: str, *args: Any, lowercase_cols: bool = False, **kwargs: Any
) -> pd.DataFrame:
    """
    Read a file and return a :class:`pandas.DataFrame`.

    Parameters
    ----------
    fname
        Path from which to read data

    lowercase_cols
        If True, convert the column names of the file to lowercase

    *args
        Passed to :func:`pandas.read_excel` if :obj:`fname` ends with '.xls' or
        '.xslx, otherwise passed to :func:`pandas.read_csv`.

    **kwargs
        Passed to :func:`pandas.read_excel` if :obj:`fname` ends with '.xls' or
        '.xslx, otherwise passed to :func:`pandas.read_csv`.

    Returns
    -------
    :class:`pandas.DataFrame`
        Read data

    Raises
    ------
    OSError
        Path specified by :obj:`fname` does not exist
    """
    is_remote = pandas.io.common.is_url(fname)
    if not is_remote and not os.path.exists(fname):
        raise OSError(f"no data file `{fname}` found!")

    if fname.endswith("xlsx") or fname.endswith("xls"):
        _logger.debug("Assuming excel file")
        xl = pd.ExcelFile(fname)

        if len(xl.sheet_names) > 1 and "sheet_name" not in kwargs:
            kwargs["sheet_name"] = "data"

        dateframe: pd.DataFrame = pd.read_excel(fname, *args, **kwargs)

    else:
        _logger.debug("Reading with pandas read_csv")
        dateframe = pd.read_csv(fname, *args, **kwargs)

    def _to_lower(c):
        if hasattr(c, "lower"):
            return c.lower()
        return c

    if lowercase_cols:
        dateframe.columns = [_to_lower(c) for c in dateframe.columns]

    return dateframe


def _format_data(  # pylint: disable=missing-return-doc
    input_df: pd.DataFrame | pd.Series, required_cols: Sequence[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare data to initialize :class:`ScmRun <scmdata.run.ScmRun>`

    Handles inut from from :class:`pandas.DataFrame` or  :class:`pandas.Series`.

    See docstring of :func:`ScmRun.__init__` for details.

    Parameters
    ----------
    df
        Data to format.

    Returns
    -------
    :class:`pandas.DataFrame`, :class:`pandas.DataFrame`
        First dataframe is the data. Second dataframe is metadata.

    Raises
    ------
    ValueError
        Not all required metadata columns are present or the time axis cannot be
        understood
    """
    df: pd.DataFrame = (
        input_df.to_frame() if isinstance(input_df, pd.Series) else input_df
    )

    # reset the index if meaningful entries are included there
    if list(df.index.names) != [None]:
        df.reset_index(inplace=True)

    if not set(required_cols).issubset(set(df.columns)):
        missing = list(set(required_cols) - set(df.columns))
        raise MissingRequiredColumnError(missing)

    # check whether data in wide or long format
    if "value" in df.columns:
        df, meta = _format_long_data(df, required_cols)
    else:
        df, meta = _format_wide_data(df, required_cols)

    return df, meta


def _format_long_data(
    df: pd.DataFrame, required_cols: Sequence[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    # check if time column is given as `year` (int) or `time` (datetime)
    cols = set(df.columns)
    if "year" in cols and "time" not in cols:
        time_col = "year"
    elif "time" in cols and "year" not in cols:
        time_col = "time"
    else:
        msg = "invalid time format, must have either `year` or `time`!"
        raise ValueError(msg)

    required_cols = list(required_cols)
    extra_cols = list(set(cols) - set([*required_cols, time_col, "value"]))
    df = df.pivot_table(columns=required_cols + extra_cols, index=time_col).value
    meta = df.columns.to_frame(index=None)
    df.columns = meta.index

    return df, meta


def _format_wide_data(
    df: pd.DataFrame, required_cols: Sequence[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cols = set(df.columns) - set(required_cols)
    time_cols = False
    extra_cols: list[str] = []

    for i in cols:
        # if in wide format, check if columns are years (int) or datetime
        if isinstance(i, (dt.datetime, cftime.datetime)):
            time_cols = True
        else:
            try:
                float(i)
                time_cols = True
            except (ValueError, TypeError):
                try:
                    try:
                        # most common format
                        dt.datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        # this is super slow so avoid if possible
                        parser.parse(str(i))  # if no ValueError, this is datetime
                    time_cols = True
                except ValueError:
                    extra_cols.append(i)  # some other string

    if not time_cols:
        msg = (
            "invalid column format, must contain some time (int, float or datetime) "
            "columns!"
        )
        raise ValueError(msg)

    all_cols_set = set(tuple(required_cols) + tuple(extra_cols))
    all_cols = list(all_cols_set)

    df_out = df.drop(all_cols, axis="columns").T
    df_out.index.name = "time"
    meta = df[all_cols].set_index(df_out.columns)

    return df_out, meta


def _from_ts(
    input_df: Any,
    required_cols: tuple[str, ...],
    index: Any = None,
    **columns: MetadataValue | Iterable[MetadataValue],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare data to initialize :class:`ScmRun <scmdata.run.ScmRun>` from wide timeseries.

    See docstring of :func:`ScmRun.__init__` for details.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        First dataframe is the data. Second dataframe is metadata

    Raises
    ------
    ValueError
        Not all required columns are present
    """
    if not isinstance(input_df, pd.DataFrame):
        input_df = pd.DataFrame(input_df)
    if index is not None:
        if isinstance(index, np.ndarray):
            input_df.index = TimePoints(index).to_index()
        elif isinstance(index, TimePoints):
            input_df.index = index.to_index()
        else:
            input_df.index = index

    # format columns to lower-case and check that all required columns exist
    if not set(required_cols).issubset(columns.keys()):
        missing = list(set(required_cols) - set(columns.keys()))
        raise MissingRequiredColumnError(missing)

    input_df.index.name = "time"

    num_ts = len(input_df.columns)
    for c_name, col in columns.items():
        col_list = (
            [col] if isinstance(col, str) or not isinstance(col, Iterable) else col
        )

        if len(col_list) == num_ts:
            continue
        if len(col_list) != 1:
            error_msg = (
                f"Length of column '{c_name}' is incorrect. It should be length "
                f"1 or {num_ts}"
            )
            raise ValueError(error_msg)
        columns[c_name] = col_list * num_ts

    meta = pd.DataFrame(columns, index=input_df.columns)

    return input_df, meta


def _get_target(run: GenericRun, inplace: bool) -> GenericRun:
    if inplace:
        return run
    else:
        return run.copy()


class BaseScmRun(OpsMixin):  # pylint: disable=too-many-public-methods
    """
    Base class of a data container for timeseries data
    """

    required_cols: tuple[str, ...] = ("variable", "unit")
    """
    Required metadata columns

    This is the bare minimum columns which are expected. Attempting to create a run
    without the metadata columns specified by :attr:`required_cols` will raise a
    MissingRequiredColumnError
    """

    data_hierarchy_separator = HIERARCHY_SEPARATOR
    """
    str: String used to define different levels in our data hierarchies.

    By default we follow pyam and use "|". In such a case, emissions of |CO2| for
    energy from coal would be "Emissions|CO2|Energy|Coal".
    """

    def __init__(
        self,
        data: Any = None,
        index: Any = None,
        columns: Mapping[str, MetadataValue | Iterable[MetadataValue]] | None = None,
        metadata: MetadataType | None = None,
        copy_data: bool = False,
        **kwargs: Any,
    ):
        """
        Initialize the container with timeseries data.

        Parameters
        ----------
        data: Union[ScmRun, IamDataFrame, pd.DataFrame, np.ndarray, str, pathlib.Path]
            If a :class:`ScmRun <scmdata.run.ScmRun>` object is provided, then a new
            :class:`ScmRun <scmdata.run.ScmRun>` is created with a copy of the values and metadata from :obj:
            `data`.

            A :class:`pandas.DataFrame` with IAMC-format data columns (the result from
            :func:`ScmRun.timeseries()`) can be provided without any additional
            :obj:`columns` and :obj:`index` information.

            If a numpy array of timeseries data is provided, :obj:`columns` and
            :obj:`index` must also be specified. The shape of the numpy array should be
            ``(n_times, n_series)`` where `n_times` is the number of timesteps and
            `n_series` is the number of time series.

            If a string or :class:`pathlib.Path` is passed, data will be attempted to be
            read from file.

            Currently, reading from CSV, gzipped CSV and Excel formatted files is
            supported. The string could be a URL in a format handled by pandas.
            Valid URL schemes include http, ftp, s3, gs, and file if pandas>1.2
            is used. For more information about the remote formats that can be read,
            see the ``pd.read_csv`` documentation for the version of pandas
            which is installed.

            If no data is provided than an empty :class:`ScmRun <scmdata.run.ScmRun>`
            object is created.

        index: np.ndarray
            If :obj:`index` is not ``None``, then the :obj:`index` is used as the timesteps
            for run. All timeseries in the run use the same set of timesteps.

            The values will be attempted to be converted to :class:`numpy.datetime[s]` values.
            Possible input formats include :

            * :class:`datetime.datetime`
            * :obj:`int` Start of year
            * :obj:`float` Decimal year
            * :obj:`str` Uses :func:`dateutil.parser`. Slow and should be avoided if possible

            If :obj:`index` is ``None``, than the time index will be obtained from the
            :obj:`data` if possible.

        columns
            If None, ScmRun will attempt to infer the values from the source.
            Otherwise, use this dict to write the metadata for each timeseries in data.
            For each metadata key (e.g. "model", "scenario"), an array of values (one
            per time series) is expected. Alternatively, providing a list of length 1
            applies the same value to all timeseries in data. For example, if you had
            three timeseries from 'rcp26' for 3 different models 'model', 'model2' and
            'model3', the column dict would look like either 'col_1' or 'col_2':

            .. code:: python

                >>> d = [[1, 2, 3]]
                >>> index = [2010]
                >>> col_1 = {
                ...     "scenario": ["rcp26"],
                ...     "model": ["model1", "model2", "model3"],
                ...     "region": ["unspecified"],
                ...     "variable": ["unspecified"],
                ...     "unit": ["unspecified"],
                ... }
                >>> single_value_init = ScmRun(d, index, columns=col_1)
                >>> col_2 = {
                ...     "scenario": ["rcp26", "rcp26", "rcp26"],
                ...     "model": ["model1", "model2", "model3"],
                ...     "region": ["unspecified"],
                ...     "variable": ["unspecified"],
                ...     "unit": ["unspecified"],
                ... }
                >>> multi_value_init = ScmRun(d, index, columns=col_2)
                >>> pd.testing.assert_frame_equal(
                ...     single_value_init.meta, multi_value_init.meta
                ... )

        metadata:
            Optional dictionary of metadata for instance as a whole.

            This can be used to store information such as the longer-form information
            about a particular dataset, for example, dataset description or DOIs.

            Defaults to an empty :obj:`dict` if no default metadata are provided.

        copy_data: bool
            If True, an explicit copy of data is performed.

            .. note::
                The copy can be very expensive on large timeseries and should only be needed
                in cases where the original data is manipulated.

        **kwargs:
            Additional parameters passed to :func:`_read_file` to read files

        Raises
        ------
        ValueError
            * If you try to load from multiple files at once. If you wish to do this,
                please use :func:`scmdata.run.run_append` instead.
            * Not specifying :obj:`index` and :obj:`columns` if :obj:`data` is a
                :class:`numpy.ndarray`

        :class:`scmdata.errors.MissingRequiredColumn`
            If metadata for :attr:`required_cols` is not found

        TypeError
            Timeseries cannot be read from :obj:`data`
        """
        if isinstance(data, ScmRun):
            self._df: pd.DataFrame = data._df.copy() if copy_data else data._df
            self._meta: pd.MultiIndex = data._meta
            self._time_points = TimePoints(data.time_points.values)
            if metadata is None:
                metadata = data.metadata.copy()
        elif data is not None:
            if copy_data and hasattr(data, "copy"):
                data = data.copy()
            self._init_timeseries(data, index, columns, copy_data=copy_data, **kwargs)
        else:
            self._df = pd.DataFrame(dtype=float)
            self._meta = pd.MultiIndex.from_frame(
                pd.DataFrame(data=[], columns=list(self.required_cols))
            )
            self._time_points = TimePoints([])

        if self._duplicated_meta():
            raise NonUniqueMetadataError(self.meta)

        self.metadata: MetadataType = metadata.copy() if metadata is not None else {}

    def _init_timeseries(
        self,
        data: Any,
        index: Any = None,
        columns: Mapping[str, Iterable[MetadataValue] | MetadataValue] | None = None,
        copy_data: bool = False,
        **kwargs: Any,
    ) -> None:
        # Lazy load
        from .pyam_compat import IamDataFrame

        if isinstance(data, np.ndarray):
            if columns is None:
                raise ValueError("`columns` argument is required")
            if index is None:
                raise ValueError("`index` argument is required")

        if columns is not None:
            (_df, _meta) = _from_ts(
                data, index=index, required_cols=self.required_cols, **columns
            )
        elif isinstance(data, (pd.DataFrame, pd.Series)):
            (_df, _meta) = _format_data(data, self.required_cols)
        elif (IamDataFrame is not None) and isinstance(data, IamDataFrame):
            (_df, _meta) = _format_data(
                data.data.copy() if copy_data else data.data, self.required_cols
            )
        else:
            if not isinstance(data, (str, pathlib.PurePath)):
                if isinstance(data, (list, tuple)) and isinstance(
                    data[0], (str, pathlib.PurePath)
                ):
                    raise ValueError(  # noqa: TRY004
                        "Initialising from multiple files not supported, "
                        "use `scmdata.run.ScmRun.append()`"
                    )
                error_msg = f"Cannot load {type(self)} from {type(data)}"
                raise TypeError(error_msg)

            (_df, _meta) = _read_file(data, required_cols=self.required_cols, **kwargs)

        if _df.index.duplicated().any():
            raise DuplicateTimesError(_df.index)

        # use :class:`TimePoints` to sort times before continuing
        _df.index = TimePoints(_df.index.values).to_index()
        _df = _df.sort_index()

        _df = _df.astype(float)
        self._df = _df
        # set time points using the sorted times
        self._time_points = TimePoints(_df.index.values)
        self._meta = pd.MultiIndex.from_frame(_meta.astype("category"))

    def copy(self) -> Self:
        """
        Return a :func:`copy.deepcopy` of self.

        Also creates copies the underlying Timeseries data

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            :func:`copy.deepcopy` of ``self``
        """
        ret = copy.copy(self)
        ret._df = self._df.copy()
        ret._meta = self._meta.copy()
        ret.metadata = copy.copy(self.metadata)

        return ret

    def __len__(self) -> int:
        """
        Get the number of timeseries.
        """
        return self._df.shape[1]

    def __getitem__(self, key: Any) -> Any:
        """
        Get item of self with helpful direct access.

        Provides direct access to "time", "year" as well as the columns in :attr:`meta`.
        If key is anything else, the key will be applied to :attr:`_data`.
        """
        _key_check = (
            [key] if isinstance(key, str) or not isinstance(key, Iterable) else key
        )
        if key == "time":
            return pd.Series(self._time_points.to_index(), dtype="object")
        if key == "year":
            return pd.Series(self._time_points.years())
        if set(_key_check).issubset(self.meta_attributes):
            try:
                return self._meta_column(key).astype(
                    self._meta_column(key).cat.categories.dtype
                )
            except ValueError:
                return self._meta_column(key).astype(float)

        raise KeyError(f"[{key}] is not in metadata")

    def __setitem__(
        self,
        key: str,
        value: Iterable[MetadataValue] | MetadataValue | None,
    ) -> Any:
        """
        Update metadata

        Parameters
        ----------
        key
            Column name

        value
            Values to write

            If a list of values is provided, then the length of that :obj:`value` must
            be the same as the number of timeseries

        Raises
        ------
        ValueError
            If the length of :obj:`meta` is inconsistent with the number of timeseries
        """
        meta = np.atleast_1d(value)  # type: ignore
        if key == "time":
            self._time_points = TimePoints(meta)
            self._df.index = self._time_points.to_index()
        elif len(meta) in (1, len(self)):
            # build new index
            new_levels = list(self._meta.levels)
            new_codes = list(self._meta.codes)
            new_names = list(self._meta.names)
            meta_ci = pd.CategoricalIndex(data=meta, name=key)
            if len(meta) == 1:
                codes = np.zeros(len(self), dtype=int)
            else:
                codes = meta_ci.codes
                meta_ci = pd.CategoricalIndex(
                    data=meta_ci.categories, categories=meta_ci.categories, name=key
                )
            if key in new_names:
                key_i = new_names.index(key)
                new_levels[key_i] = meta_ci
                new_codes[key_i] = codes
            else:
                new_names.append(key)
                new_levels.append(meta_ci)
                new_codes.append(codes)
            self._meta = pd.MultiIndex(
                levels=new_levels,
                codes=new_codes,
                names=new_names,
                verify_integrity=False,
            )
        else:
            msg = (
                "Invalid length for metadata, `{}`, must be 1 or equal to the "
                "number of timeseries, `{}`"
            )
            raise ValueError(msg.format(len(meta), len(self)))

        if self._duplicated_meta():
            raise NonUniqueMetadataError(self.meta)

    def __repr__(self):
        """Generate a repr string"""

        def _indent(s):
            lines = ["\t" + line for line in s.split("\n")]
            return "\n".join(lines)

        meta_str = _indent(self.meta.__repr__())
        if len(self.time_points):
            time_str = [
                f"Start: {self.time_points.values[0]}",
                f"End: {self.time_points.values[-1]}",
            ]
        else:
            time_str = ["Start: N/A", "End: N/A"]
        time_str = _indent("\n".join(time_str))
        return "<{} (timeseries: {}, timepoints: {})>\nTime:\n{}\nMeta:\n{}".format(
            self.__class__.__name__,
            len(self),
            len(self.time_points),
            time_str,
            meta_str,
        )

    def _binary_op(
        self,
        other: Self | pint.Quantity | float | int,
        f: Callable[[pd.DataFrame, pd.DataFrame], pd.DataFrame],
        reflexive: bool = False,
        **kwargs: Any,
    ) -> Self:
        if isinstance(other, ScmRun):
            return NotImplemented

        is_scalar = isinstance(other, (numbers.Number, pint.Quantity))
        ur = scmdata.units.get_unit_registry()
        if not is_scalar:
            other_ndim = len(other.shape)
            if other_ndim == 1:
                if other.shape[0] != self.shape[1]:
                    raise ValueError(
                        "only vectors with the same number of timesteps "
                        f"as self ({self.shape[1]}) are supported"
                    )
            else:
                raise ValueError(
                    f"operations with {other_ndim}d data are not supported"
                )

        def _perform_op(run: Self) -> Self:
            if isinstance(other, pint.Quantity):
                try:
                    data = run.values * ur(run.get_unique_meta("unit", True))
                    use_pint = True
                except KeyError:  # pragma: no cover # emergency valve
                    raise KeyError(  # noqa: TRY200
                        "No `unit` column in your metadata, cannot perform operations "
                        "with pint quantities"
                    )
            else:
                data = run.values
                use_pint = False

            res = []
            for v in data:
                if not reflexive:
                    res.append(f(v, other))
                else:
                    res.append(f(other, v))
            res_stacked = np.vstack(res)

            if use_pint:
                run._df.values[:] = res_stacked.magnitude.T
                run["unit"] = str(res_stacked.units)
            else:
                run._df.values[:] = res_stacked.T
            return run

        return self.copy().groupby("unit").apply(_perform_op)

    def _unary_op(self, f: Any, *args: Any, **kwargs: Any) -> Self:
        run = self.copy()

        res = [f(v) for v in run.values]

        run._df.values[:] = np.vstack(res).T
        return run

    def drop_meta(self, columns: Iterable[str] | str, inplace: bool = False) -> Self:
        """
        Drop meta columns out of the Run

        Parameters
        ----------
        columns
            The column or columns to drop
        inplace
            If True, do operation inplace, otherwise a copy is performed.

        Raises
        ------
        KeyError
            If any of the columns do not exist in the meta :class:`DataFrame`

        Returns
        -------
            Object without the specified meta columns.
        """
        ret = _get_target(self, inplace)

        if isinstance(columns, str):
            columns = [columns]

        existing_cols = ret.meta_attributes
        for c in columns:
            if c not in existing_cols:
                raise KeyError(c)
            if c in self.required_cols:
                raise MissingRequiredColumnError([c])
        for c in columns:
            ret._meta = ret._meta.droplevel(c)

        if ret._duplicated_meta():
            raise NonUniqueMetadataError(ret.meta)

        return ret

    @property
    def meta_attributes(self):
        """
        Get a list of all meta keys

        Returns
        -------
        list
            Sorted list of meta keys
        """
        return sorted(list(self._meta.names))

    @property
    def time_points(self):
        """
        Time points of the data

        Returns
        -------
        :class:`scmdata.time.TimePoints`
        """
        return self._time_points

    def timeseries(
        self,
        meta: Iterable[str] | None = None,
        check_duplicated: bool = True,
        time_axis: str | None = None,
        drop_all_nan_times: bool = False,
    ) -> pd.DataFrame:
        """
        Return the data with metadata as a :class:`pandas.DataFrame`.

        Parameters
        ----------
        meta : list[str]
            The list of meta columns that will be included in the output's
            MultiIndex. If None (default), then all metadata will be used.

        check_duplicated : bool
            If True, an exception is raised if any of the timeseries have
            duplicated metadata

        time_axis : {None, "year", "year-month", "days since 1970-01-01", "seconds since 1970-01-01"}
            See :func:`long_data` for a description of the options.

        drop_all_nan_times : bool
            Should time points which contain only nan values be dropped? This operation is applied
            after any transforms introduced by the value of ``time_axis``.

        Returns
        -------
        :class:`pandas.DataFrame`
            DataFrame with datetimes as columns and timeseries as rows.
            Metadata is in the index.

        Raises
        ------
        :class:`NonUniqueMetadataError`
            If the metadata are not unique between timeseries and
            ``check_duplicated`` is ``True``

        NotImplementedError
            The value of `time_axis` is not recognised

        ValueError
            The value of `time_axis` would result in columns which aren't unique
        """
        df = self._df.T
        _meta = self.meta if meta is None else self.meta[meta]

        if check_duplicated and self._duplicated_meta(meta=_meta):
            raise NonUniqueMetadataError(_meta)

        if time_axis is None:
            columns = self._time_points.to_index().infer_objects()
        elif time_axis == "year":
            columns = self._time_points.years()
        elif time_axis == "year-month":
            columns = (
                self._time_points.years() + (self._time_points.months() - 0.5) / 12
            )
        elif time_axis == "days since 1970-01-01":

            def calc_days(x):
                ref = np.array(["1970-01-01"], dtype=_TARGET_DTYPE)[0]

                return (x - ref).astype("timedelta64[D]")

            columns = calc_days(self._time_points.values).astype(int)

        elif time_axis == "seconds since 1970-01-01":

            def calc_seconds(x):
                ref = np.array(["1970-01-01"], dtype=_TARGET_DTYPE)[0]

                return x - ref

            columns = calc_seconds(self._time_points.values).astype(int)

        else:
            raise NotImplementedError(f"time_axis = '{time_axis}'")

        if len(np.unique(columns)) != len(columns):
            raise ValueError(f"Ambiguous time values with time_axis = '{time_axis}'")

        df.index = pd.MultiIndex.from_frame(_meta)
        if isinstance(columns, pd.Index):
            df.columns = columns
        else:
            df.columns = pd.Index(columns, name="time")

        if drop_all_nan_times:
            df = df.dropna(how="all", axis="columns")

        return df

    def _duplicated_meta(self, meta=None):
        _meta = self._meta if meta is None else meta

        return _meta.duplicated().any()

    def long_data(self, time_axis=None):
        """
        Return data in long form, particularly useful for plotting with seaborn

        Parameters
        ----------
        time_axis : {None, "year", "year-month", "days since 1970-01-01", "seconds since 1970-01-01"}
            Time axis to use for the output's columns.

            If ``None``, :class:`datetime.datetime` objects will be used.

            If ``"year"``, the year of each time point  will be used.

            If ``"year-month"``, the year plus (month - 0.5) / 12  will be used.

            If ``"days since 1970-01-01"``, the number of days  since 1st Jan 1970
            will be used (calculated using the :mod:`datetime`  module).

            If ``"seconds since 1970-01-01"``, the number of seconds  since 1st Jan
            1970 will be used (calculated using the :mod:`datetime` module).

        Returns
        -------
        :class:`pandas.DataFrame`
            :class:`pandas.DataFrame` containing the data in 'long form' (i.e. one observation
            per row).
        """
        out: pd.DataFrame = self.timeseries(time_axis=time_axis).stack()  # type: ignore
        out.name = "value"
        result = out.to_frame().reset_index()

        return result

    @property
    def shape(self) -> tuple[int, int]:
        """
        Get the shape of the underlying data as ``(num_timeseries, num_timesteps)``

        Returns
        -------
        tuple of int
        """
        return self._df.T.shape

    @property
    def values(self) -> NDArray[np.float_]:
        """
        Timeseries values without metadata

        The values are returned such that each row is a different
        timeseries being a row and each column is a different time (although
        no time information is included as a plain :class:`numpy.ndarray` is
        returned).

        Returns
        -------
        np.ndarray
            The array in the same shape as :meth:`ScmRun.shape`, that is
            ``(num_timeseries, num_timesteps)``.
        """
        return self._df.values.T

    @property
    def empty(self) -> bool:
        """
        Indicate whether :class:`ScmRun <scmdata.run.ScmRun>` is empty i.e. contains no data

        Returns
        -------
        bool
            If :class:`ScmRun <scmdata.run.ScmRun>` is empty, return ``True``, if not return ``False``
        """
        return len(self) == 0

    @property
    def meta(self) -> pd.DataFrame:
        """
        Metadata
        """
        df = pd.DataFrame(
            self._meta.to_list(), columns=self._meta.names, index=self._df.columns
        )

        return df[sorted(df.columns)]

    def _meta_column(self, col: str) -> pd.Series:
        out = self._meta.get_level_values(col)
        return pd.Series(out, name=col, index=self._df.columns)

    def set_meta(
        self,
        dimension: str,
        value: MetadataValue | Iterable[MetadataValue],
        **filter_kwargs: MetadataValue | Iterable[MetadataValue],
    ) -> Self:
        """
        Update metadata

        Optionally, a subset of metadata may be modified through the use of
        additional `filter_kwargs` which are passed to :func:`filter`. The metadata
        associated with the non-filtered timeseries are not modified.

        This method does not preserve the order of the timeseries.

        Parameters
        ----------
        dimension : str
            Dimension of meta to update

        value : Any
            Value to set the targeted meta to

        filter_kwargs : Any
            Arguments used to filter which timeseries are updated

            All the filtering functionality of :func:`filter` is available, except for
            `"inplace"`.

        See Also
        --------
        :func:`filter`

        Returns
        -------
        :class:`BaseScmRun <scmdata.run.BaseScmRun>`
            A new instance with the updated metadata.
        """
        keep: bool = filter_kwargs.pop("keep", True)
        log_if_empty = filter_kwargs.pop("log_if_empty", True)

        if "inplace" in filter_kwargs:
            raise ValueError("Inplace updating of metadata is not supported")

        filtered_run = self.filter(
            keep=keep, log_if_empty=log_if_empty, **filter_kwargs
        )
        filtered_run[dimension] = value
        res = run_append(
            [
                filtered_run,
                self.filter(keep=not keep, log_if_empty=False, **filter_kwargs),
            ]
        )

        return res

    def filter(
        self,
        *,
        keep: bool = True,
        inplace: bool = False,
        log_if_empty: bool = True,
        # mypy doesn't really support mapping unpacking https://github.com/python/mypy/issues/11583
        **kwargs: MetadataValue | Iterable[MetadataValue],
    ) -> Self:
        """
        Return a filtered ScmRun (i.e., a subset of the data).

        .. code:: python

            >>> from scmdata import ScmRun
            >>> df = ScmRun(
            ...     data=[[1, 2, 3], [4, 5, 6], [3, 3, 1]],
            ...     index=[2005, 2010, 2015],
            ...     columns={
            ...         "model": "a_iam",
            ...         "scenario": ["a_scenario", "a_scenario", "a_scenario2"],
            ...         "region": "World",
            ...         "variable": [
            ...             "Primary Energy",
            ...             "Primary Energy|Coal",
            ...             "Primary Energy",
            ...         ],
            ...         "unit": "EJ/yr",
            ...     },
            ... )
            >>> df
            <ScmRun (timeseries: 3, timepoints: 3)>
            Time:
                Start: 2005-01-01T00:00:00
                End: 2015-01-01T00:00:00
            Meta:
                   model region     scenario   unit             variable
                0  a_iam  World   a_scenario  EJ/yr       Primary Energy
                1  a_iam  World   a_scenario  EJ/yr  Primary Energy|Coal
                2  a_iam  World  a_scenario2  EJ/yr       Primary Energy

            >>> df.filter(scenario="a_scenario")
            <ScmRun (timeseries: 2, timepoints: 3)>
            Time:
                Start: 2005-01-01T00:00:00
                End: 2015-01-01T00:00:00
            Meta:
                   model region    scenario   unit             variable
                0  a_iam  World  a_scenario  EJ/yr       Primary Energy
                1  a_iam  World  a_scenario  EJ/yr  Primary Energy|Coal

            >>> df.filter(scenario="a_scenario", keep=False)
            <ScmRun (timeseries: 1, timepoints: 3)>
            Time:
                Start: 2005-01-01T00:00:00
                End: 2015-01-01T00:00:00
            Meta:
                   model region     scenario   unit        variable
                2  a_iam  World  a_scenario2  EJ/yr  Primary Energy

            >>> df.filter(level=1)
            <ScmRun (timeseries: 1, timepoints: 3)>
            Time:
                Start: 2005-01-01T00:00:00
                End: 2015-01-01T00:00:00
            Meta:
                   model region    scenario   unit             variable
                1  a_iam  World  a_scenario  EJ/yr  Primary Energy|Coal

            >>> df.filter(year=range(2000, 2011))
            <ScmRun (timeseries: 3, timepoints: 2)>
            Time:
                Start: 2005-01-01T00:00:00
                End: 2010-01-01T00:00:00
            Meta:
                   model region     scenario   unit             variable
                0  a_iam  World   a_scenario  EJ/yr       Primary Energy
                1  a_iam  World   a_scenario  EJ/yr  Primary Energy|Coal
                2  a_iam  World  a_scenario2  EJ/yr       Primary Energy

        Parameters
        ----------
        keep
            If True, keep all timeseries satisfying the filters, otherwise drop all the
            timeseries satisfying the filters

        inplace
            If True, do operation inplace, otherwise a copy is performed.

        log_if_empty
            If ``True``, log a warning level message if the result is empty.

        **kwargs
            Argument names are keys with which to filter, values are used to do the
            filtering. Filtering can be done on:

            - all metadata columns with strings, "*" can be used as a wildcard in search
              strings

            - 'level': the maximum "depth" of IAM variables (number of hierarchy levels,
              excluding the strings given in the 'variable' argument)

            - 'time': takes a :class:`datetime.datetime` or list of
              :class:`datetime.datetime`'s
              TODO: default to np.datetime64

            - 'year', 'month', 'day', hour': takes an :obj:`int` or list of
              :obj:`int`'s ('month' and 'day' also accept :obj:`str` or list of
              :obj:`str`)

            If ``regexp=True`` is included in :obj:`kwargs` then the pseudo-regexp
            syntax in :func:`pattern_match` is disabled.

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            Object containing a filtered subset of timeseries.
        """
        ret = copy.copy(self) if not inplace else self

        _keep_times, _keep_rows = self._apply_filters(kwargs)
        if (
            not keep
            and len(_keep_rows)
            and len(_keep_times)
            and sum(~_keep_rows)
            and sum(~_keep_times)
        ):
            raise ValueError(
                "If keep==False, filtering cannot be performed on the temporal axis "
                "and with metadata at the same time"
            )

        reduce_times = len(_keep_times) and (~_keep_times).sum() > 0
        reduce_rows = len(_keep_rows) and (~_keep_rows).sum() > 0

        if not keep:
            if reduce_times:
                _keep_times = ~_keep_times
            if reduce_rows:
                _keep_rows = ~_keep_rows
            if not reduce_rows and not reduce_times:
                _keep_times = _keep_times * False
                _keep_rows = _keep_rows * False

        ret._df = ret._df.loc[_keep_times, _keep_rows]
        if len(_keep_rows):
            ret._meta = ret._meta[_keep_rows]
        if len(_keep_times):
            ret["time"] = self.time_points.values[_keep_times]

        if log_if_empty and ret.empty:
            _logger.warning("Filtered ScmRun is empty!", stack_info=True)

        return ret

    def _apply_filters(  # noqa: PLR0912
        self, filters: dict[str, MetadataValue | Iterable[MetadataValue]]
    ) -> tuple[NDArray[np.bool_], NDArray[np.bool_]]:
        """
        Determine rows to keep in data for given set of filters.

        Parameters
        ----------
        filters
            Dictionary of filters ``({col: values}})``; uses a pseudo-regexp syntax by
            default but if ``filters["regexp"]`` is ``True``, regexp is used directly.

        Returns
        -------
        :class:`numpy.ndarray` of :class:`bool`, :class:`numpy.ndarray` of :class:`bool`
            Two boolean :class:`numpy.ndarray`'s. The first contains the columns to keep
            (i.e. which time points to keep). The second contains the rows to keep (i.e.
            which metadata matched the filters).

        Raises
        ------
        ValueError
            Filtering cannot be performed on requested column
        """
        regexp: bool = filters.pop("regexp", False)
        keep_ts = np.array([True] * len(self.time_points))
        keep_meta = np.array([True] * len(self))

        time_filter_options = ["year", "month", "day", "hour", "time"]

        # filter by columns and list of values
        for col, values in filters.items():
            if not len(keep_ts) and col in time_filter_options:
                continue

            if col in self._meta.names:
                if col == "variable":
                    level = filters["level"] if "level" in filters else None
                else:
                    level = None
                if not len(keep_meta):
                    continue

                keep_meta &= pattern_match(
                    self._meta.get_level_values(col),
                    values,
                    level=level,
                    regexp=regexp,
                    separator=self.data_hierarchy_separator,
                )

            elif col == "level":
                if "variable" not in filters.keys() and len(keep_meta):
                    keep_meta &= pattern_match(
                        self._meta.get_level_values("variable"),
                        "*",
                        level=values,
                        regexp=regexp,
                        separator=self.data_hierarchy_separator,
                    )
                # else do nothing as level handled in variable filtering

            elif col == "year":
                keep_ts &= years_match(self._time_points.years(), values)

            elif col == "month":
                keep_ts &= month_match(self._time_points.months(), values)

            elif col == "day":
                keep_ts &= self._day_match(values)

            elif col == "hour":
                keep_ts &= hour_match(self._time_points.hours(), values)

            elif col == "time":
                keep_ts &= datetime_match(self._time_points.values, values)

            else:
                raise ValueError(f"filter by `{col}` not supported")

        return keep_ts, keep_meta

    def _day_match(self, values):
        if isinstance(values, str):
            wday = True
        elif isinstance(values, list) and isinstance(values[0], str):
            wday = True
        else:
            wday = False

        if wday:
            days = self._time_points.weekdays()
        else:  # ints or list of ints
            days = self._time_points.days()

        return day_match(days, values)

    def head(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """
        Return head of :func:`self.timeseries()`.

        Parameters
        ----------
        *args
            Passed to :func:`self.timeseries().head()`

        **kwargs
            Passed to :func:`self.timeseries().head()`

        Returns
        -------
        :class:`pandas.DataFrame`
            Tail of :func:`self.timeseries()`
        """
        return self.timeseries().head(*args, **kwargs)  # type: ignore

    def tail(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """
        Return tail of :func:`self.timeseries()`.

        Parameters
        ----------
        *args
            Passed to :func:`self.timeseries().tail()`

        **kwargs
            Passed to :func:`self.timeseries().tail()`

        Returns
        -------
        :class:`pandas.DataFrame`
            Tail of :func:`self.timeseries()`
        """
        return self.timeseries().tail(*args, **kwargs)  # type: ignore

    @overload
    def get_unique_meta(
        self,
        meta: str,
        no_duplicates: Literal[True],
    ) -> MetadataValue:
        ...

    @overload
    def get_unique_meta(
        self,
        meta: str,
        no_duplicates: Literal[False] = ...,
    ) -> list[MetadataValue]:
        ...

    def get_unique_meta(
        self,
        meta: str,
        no_duplicates: bool | None = False,
    ) -> list[MetadataValue] | MetadataValue:
        """
        Get unique values in a metadata column.

        Parameters
        ----------
        meta
            Column to retrieve metadata for

        no_duplicates
            Should I raise an error if there is more than one unique value in the
            metadata column?

        Raises
        ------
        ValueError
            There is more than one unique value in the metadata column and
            ``no_duplicates`` is ``True``.

        KeyError
            If a ``meta`` column does not exist in the run's metadata

        Returns
        -------
        [List[Any], Any]
            List of unique metadata values. If ``no_duplicates`` is ``True`` the
            metadata value will be returned (rather than a list).
        """
        vals: list[MetadataValue] = self._meta.get_level_values(meta).unique().to_list()
        if no_duplicates:
            if len(vals) != 1:
                raise ValueError(
                    f"`{meta}` column is not unique (found values: {vals})"
                )

            return vals[0]

        return vals

    def interpolate(
        self,
        target_times: Iterable[dt.datetime | (dt.date | (int | float))],
        interpolation_type: str = "linear",
        extrapolation_type: str | None = "linear",
        uniform_year_length: bool = False,
    ) -> Self:
        """
        Interpolate the data onto a new time frame.

        Parameters
        ----------
        target_times
            Time grid onto which to interpolate
        interpolation_type: str
            Interpolation type. Options are 'linear'
        extrapolation_type: str or None
            Extrapolation type. Options are None, 'linear' or 'constant'
        uniform_year_length: bool
            If True, a 365-day calendar is assumed where each year has an equal length

            By default, the interpolation takes into account the different number of
            days in leap years.

        Raises
        ------
        ValueError
            If ``uniform_year_length=True`` and sub-annual timeseries are present

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            A new :class:`ScmRun <scmdata.run.ScmRun>` containing the data interpolated onto the
            :obj:`target_times` grid
        """
        # pylint: disable=protected-access
        target_time_points: TimePoints = TimePoints(target_times)
        source_times_points: TimePoints = self.time_points

        if uniform_year_length:
            source_time_values = source_times_points.years()

            if len(np.unique(source_time_values)) != len(source_times_points):
                raise ValueError("Non-unique year values with uniform_year_length=True")
            target_time_values = target_time_points.years()
        else:
            source_time_values = source_times_points.values
            target_time_values = target_time_points.values

        res = self.copy()

        timeseries_converter = TimeseriesConverter(
            source_time_values,
            target_time_values,
            interpolation_type=interpolation_type,
            extrapolation_type=extrapolation_type,
        )
        target_data = np.zeros((len(target_time_points), len(res)))

        # TODO: Extend TimeseriesConverter to handle 2d inputs
        for i in range(len(res)):
            target_data[:, i] = timeseries_converter.convert_from(
                res._df.iloc[:, i].values
            )
        res._df = pd.DataFrame(
            target_data, columns=res._df.columns, index=target_time_points.to_index()
        )
        res._time_points = target_time_points

        return res

    def resample(self, rule: str = "AS", **kwargs: Any) -> Self:
        """
        Resample the time index of the timeseries data onto a custom grid.

        This helper function allows for values to be easily interpolated onto annual or
        monthly timesteps using the rules='AS' or 'MS' respectively. Internally, the
        interpolate function performs the regridding.

        Parameters
        ----------
        rule
            See the pandas `user guide
            <http://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects>`_
            for a list of options. Note that Business-related offsets such as
            "BusinessDay" are not supported.

        **kwargs
            Other arguments to pass through to :func:`interpolate`

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            New :class:`ScmRun <scmdata.run.ScmRun>` instance on a new time index

        Examples
        --------
        Resample a run to annual values

        >>> scm_df = ScmRun(
        ...     pd.Series([1, 2, 10], index=(2000, 2001, 2009)),
        ...     columns={
        ...         "model": ["a_iam"],
        ...         "scenario": ["a_scenario"],
        ...         "region": ["World"],
        ...         "variable": ["Primary Energy"],
        ...         "unit": ["EJ/y"],
        ...     },
        ... )
        >>> scm_df.timeseries().T  # doctest: +NORMALIZE_WHITESPACE
        model               a_iam
        region              World
        scenario       a_scenario
        unit                 EJ/y
        variable   Primary Energy
        time
        2000-01-01            1.0
        2001-01-01            2.0
        2009-01-01           10.0

        An annual timeseries can be the created by interpolating to the start of years
        using the rule 'AS'.

        >>> res = scm_df.resample("AS")
        >>> res.timeseries().T
        model               a_iam
        region              World
        scenario       a_scenario
        unit                 EJ/y
        variable   Primary Energy
        time
        2000-01-01       1.000000
        2001-01-01       2.000000
        2002-01-01       2.999316
        2003-01-01       3.998631
        2004-01-01       4.997947
        2005-01-01       6.000000
        2006-01-01       6.999316
        2007-01-01       7.998631
        2008-01-01       8.997947
        2009-01-01      10.000000

        >>> m_df = scm_df.resample("MS")
        >>> m_df.timeseries().T  # doctest: +ELLIPSIS
        model               a_iam
        region              World
        scenario       a_scenario
        unit                 EJ/y
        variable   Primary Energy
        time
        2000-01-01       1.000000
        2000-02-01       1.084699
        2000-03-01       1.163934
        ...

        Note that the values do not fall exactly on integer values as not all years are
        exactly the same length.

        References
        ----------
        See the pandas documentation for
        `resample <http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.
        Series.resample.html>`
        for more information about possible arguments.
        """
        orig_dts = self["time"]
        target_dts = generate_range(
            orig_dts.iloc[0], orig_dts.iloc[-1], to_offset(rule)
        )
        return self.interpolate(list(target_dts), **kwargs)

    def time_mean(self, rule: str) -> Self:
        """
        Take time mean of self

        Note that this method will not copy the ``metadata`` attribute to the returned
        value.

        Parameters
        ----------
        rule : ["AC", "AS", "A"]
            How to take the time mean. The names reflect the pandas
            `user guide <http://pandas.pydata.org/pandas-docs/stable/user_guide/timeser
            ies.html#dateoffset-objects>`_
            where they can, but only the options
            given above are supported. For clarity, if ``rule`` is ``'AC'``, then the
            mean is an annual mean i.e. each time point in the result is the mean of
            all values for that particular year. If ``rule`` is ``'AS'``, then the
            mean is an annual mean centred on the beginning of the year i.e. each time
            point in the result is the mean of all values from July 1st in the
            previous year to June 30 in the given year. If ``rule`` is ``'A'``, then
            the mean is an annual mean centred on the end of the year i.e. each time
            point in the result is the mean of all values from July 1st of the given
            year to June 30 in the next year.

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            The time mean of ``self``.
        """
        if rule == "AS":

            def group_annual_mean_beginning_of_year(x):
                if x.month <= 6:  # noqa: PLR2004
                    return x.year
                return x.year + 1

            ts_resampled = (
                self.timeseries()
                .T.groupby(group_annual_mean_beginning_of_year)
                .mean()
                .T
            )
            ts_resampled.columns = ts_resampled.columns.map(
                lambda x: dt.datetime(x, 1, 1)
            )
            return type(self)(ts_resampled)

        if rule == "AC":

            def group_annual_mean(x):
                return x.year

            ts_resampled = self.timeseries().T.groupby(group_annual_mean).mean().T
            ts_resampled.columns = ts_resampled.columns.map(
                lambda x: dt.datetime(x, 7, 1)
            )
            return type(self)(ts_resampled)

        if rule == "A":

            def group_annual_mean_end_of_year(x):
                if x.month >= 7:  # noqa: PLR2004
                    return x.year
                return x.year - 1

            ts_resampled = (
                self.timeseries().T.groupby(group_annual_mean_end_of_year).mean().T
            )
            ts_resampled.columns = ts_resampled.columns.map(
                lambda x: dt.datetime(x, 12, 31)
            )
            return type(self)(ts_resampled)

        raise ValueError(f"`rule` = `{rule}` is not supported")

    @overload
    def process_over(
        self,
        cols: str | list[str],
        operation: str | ApplyCallable,
        na_override: float = -1e6,
        op_cols: dict[str, str] | None = None,
        as_run: type[GenericRun] = ...,
        **kwargs: Any,
    ) -> GenericRun:
        ...

    @overload
    def process_over(
        self,
        cols: str | list[str],
        operation: str | ApplyCallable,
        na_override: float = -1e6,
        op_cols: dict[str, str] | None = None,
        as_run: Literal[False] = False,
        **kwargs: Any,
    ) -> pd.DataFrame:
        ...

    @overload
    def process_over(
        self,
        cols: str | list[str],
        operation: str | ApplyCallable,
        na_override: float = -1e6,
        op_cols: dict[str, str] | None = None,
        as_run: Literal[True] = ...,
        **kwargs: Any,
    ) -> Self:
        ...

    def process_over(  # noqa: PLR0912
        self,
        cols: str | list[str],
        operation: str | ApplyCallable,
        na_override: float = -1e6,
        op_cols: dict[str, str] | None = None,
        as_run: bool | type[GenericRun] = False,
        **kwargs: Any,
    ) -> pd.DataFrame | (Self | GenericRun):
        """
        Process the data over the input columns.

        Parameters
        ----------
        cols
            Columns to perform the operation on. The timeseries will be grouped by all
            other columns in :attr:`meta`.

        operation : str or func
            The operation to perform.

            If a string is provided, the equivalent pandas groupby function is used. Note
            that not all groupby functions are available as some do not make sense for
            this particular application. Additional information about the arguments for
            the pandas groupby functions can be found at <https://pandas.pydata.org/pan
            das-docs/stable/reference/groupby.html>`_.

            If a function is provided, it will be applied to each group. The function must
            take a dataframe as its first argument and return a DataFrame, Series or scalar.

            Note that quantile means the value of the data at a given point in the cumulative
            distribution of values at each point in the timeseries, for each timeseries
            once the groupby is applied. As a result, using ``q=0.5`` is the same as
            taking the median and not the same as taking the mean/average.

        na_override: [int, float]
            Convert any nan value in the timeseries meta to this value during processsing.
            The meta values converted back to nan's before the run is returned. This
            should not need to be changed unless the existing metadata clashes with the
            default na_override value.

            This functionality is disabled if na_override is None, but may result in incorrect
            results if the timeseries meta includes any nan's.

        op_cols: dict of str: str
            Dictionary containing any columns that should be overridden after processing.

            If a required column from :class:`scmdata.ScmRun` is specified in ``cols`` and
            ``as_run=True``, an override must be provided for that column in ``op_cols``
            otherwise the conversion to :class:`scmdata.ScmRun` will fail.

        as_run: bool or subclass of BaseScmRun
            If True, return the resulting timeseries as an :class:`scmdata.ScmRun` object,
            otherwise if False, a :class:`pandas.DataFrame`or :class:`pandas.Series` is
            returned (depending on the nature of the operation). Some operations may not be
            able to be converted to a :class:`scmdata.ScmRun`. For example if the operation
            returns scalar values rather than timeseries.

            If a class is provided, the return value will be cast to this class.
        **kwargs
            Keyword arguments to pass ``operation`` (or the pandas operation if ``operation``
            is a string)

        Returns
        -------
        :class:`pandas.DataFrame` or :class:`pandas.Series` or :class:`scmdata.ScmRun`
            The result of ``operation``, grouped by all columns in :attr:`meta`
            other than :obj:`cols`

        Raises
        ------
        ValueError
            If the operation is not an allowed operation

            If the value of na_override clashes with any existing metadata

            If ``operation`` produces a :class:`pandas.Series`, but `as_run`` is True

            If ``as_run`` is not True, False or a subclass of :class:`scmdata.run.BaseScmRun`

        :class:`scmdata.errors.MissingRequiredColumnError`
            If `as_run` is not False and the result does not have the required metadata
            to convert to an :class`ScmRun <scmdata.ScmRun>`.
            This can be resolved by specifying additional metadata via ``op_cols``

        """
        cols = [cols] if isinstance(cols, str) else cols
        ts = self.timeseries()
        if na_override is not None:
            ts_idx = ts.index.to_frame()
            if ts_idx[ts_idx == na_override].any().any():
                raise ValueError(
                    f"na_override clashes with existing meta: {na_override}"
                )
            ts.index = pd.MultiIndex.from_frame(ts_idx.fillna(na_override))

        group_cols = list(set(ts.index.names) - set(cols))
        grouper = ts.groupby(group_cols, group_keys=False)

        # This is a subset of the available functions
        #  https://pandas.pydata.org/pandas-docs/stable/reference/groupby.html
        allowed_pd_ops = [
            "count",
            "cumcount",
            "cummax",
            "cummin",
            "cumprod",
            "cumsum",
            "first",
            "last",
            "max",
            "mean",
            "median",
            "min",
            "prod",
            "rank",
            "std",
            "sum",
            "var",
            "quantile",
        ]

        if isinstance(operation, str):
            if operation not in allowed_pd_ops:
                raise ValueError("invalid process_over operation")
            grouper_func = getattr(grouper, operation)
            res = grouper_func(**kwargs)
        else:
            res = grouper.apply(operation, **kwargs)

        if op_cols is not None:
            idx_df = res.index.to_frame()
            for column_name in op_cols:
                idx_df[column_name] = op_cols[column_name]
            res.index = pd.MultiIndex.from_frame(idx_df)

        if na_override is not None:
            idx_df = res.index.to_frame()
            idx_df[idx_df == na_override] = np.nan
            res.index = pd.MultiIndex.from_frame(idx_df)

        res = res.reorder_levels(sorted(res.index.names))

        if as_run:
            if isinstance(res, pd.Series):
                raise ValueError("Cannot convert pd.Series to ScmRun")
            if isinstance(as_run, bool):
                Cls = self.__class__
            elif issubclass(as_run, BaseScmRun):
                Cls = as_run
            else:
                raise ValueError(
                    "Invalid value for as_run. Expected True, False or class based on scmdata.run.BaseScmRun"
                )

            return Cls(res, metadata=self.metadata)
        else:
            return cast(pd.DataFrame, res)

    def quantiles_over(
        self,
        cols: str | list[str],
        quantiles: str | list[float],
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Calculate quantiles of the data over the input columns.

        Parameters
        ----------
        cols
            Columns to perform the operation on. The timeseries will be grouped by all
            other columns in :attr:`meta`.

        quantiles
            The quantiles to calculate. This should be a list of quantiles to calculate
            (quantile values between 0 and 1). ``quantiles`` can also include the strings
            "median" or "mean" if these values are to be calculated.

        **kwargs
            Passed to :meth:`~ScmRun.process_over`.

        Returns
        -------
        :class:`pandas.DataFrame`
            The quantiles of the timeseries, grouped by all columns in :attr:`meta`
            other than :obj:`cols`. Each calculated quantile is given a label which is
            stored in the ``quantile`` column within the output index.

        Raises
        ------
        TypeError
            ``operation`` is included in ``kwargs``. The operation is inferred from ``quantiles``.
        """
        if "operation" in kwargs:
            raise TypeError(
                "quantiles_over() does not take the keyword argument 'operation', the operations "
                "are inferred from the 'quantiles' argument"
            )

        out = []
        for quant in quantiles:
            if quant == "median":
                quantile_df: pd.DataFrame = self.process_over(cols, "median")
            elif quant == "mean":
                quantile_df = self.process_over(cols, "mean")
            else:
                quantile_df = self.process_over(cols, "quantile", q=quant)

            quantile_df["quantile"] = quant

            out.append(quantile_df)

        out_concat = pd.concat(out).set_index("quantile", append=True)

        return out_concat

    @staticmethod
    def _check_groupby_input(v: tuple[str | Iterable[str], ...]) -> tuple[str, ...]:
        if len(v) == 1 and not isinstance(v[0], str):
            v = tuple(v[0])

        return v  # type: ignore

    def groupby(self, *group: str | Iterable[str]) -> RunGroupBy[Self]:
        """
        Group the object by unique metadata

        Enables iteration over groups of data. For example, to iterate over each
        scenario in the object

        .. code:: python

            >>> from scmdata import ScmRun
            >>> run = ScmRun(
            ...     data=[[1, 2, 3], [4, 5, 6], [3, 3, 1]],
            ...     index=[2005, 2010, 2015],
            ...     columns={
            ...         "model": "a_iam",
            ...         "scenario": ["a_scenario", "a_scenario", "a_scenario2"],
            ...         "region": "World",
            ...         "variable": [
            ...             "Primary Energy",
            ...             "Primary Energy|Coal",
            ...             "Primary Energy",
            ...         ],
            ...         "unit": "EJ/yr",
            ...     },
            ... )

            >>> for group in run.groupby("scenario"):
            ...     print(group)
            ...
            <ScmRun (timeseries: 2, timepoints: 3)>
            Time:
                Start: 2005-01-01T00:00:00
                End: 2015-01-01T00:00:00
            Meta:
                   model region    scenario   unit             variable
                0  a_iam  World  a_scenario  EJ/yr       Primary Energy
                1  a_iam  World  a_scenario  EJ/yr  Primary Energy|Coal
            <ScmRun (timeseries: 1, timepoints: 3)>
            Time:
                Start: 2005-01-01T00:00:00
                End: 2015-01-01T00:00:00
            Meta:
                   model region     scenario   unit        variable
                2  a_iam  World  a_scenario2  EJ/yr  Primary Energy

        Parameters
        ----------
        group: str or list of str
            Columns to group by

        Returns
        -------
        :class:`RunGroupBy`
            See the documentation for :class:`RunGroupBy` for more information
        """
        from .groupby import RunGroupBy

        group = self._check_groupby_input(group)

        return RunGroupBy(self, group)

    def apply(
        self,
        func: Callable[Concatenate[Self, P], Self | (pd.DataFrame | None)],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Self | None:
        """
        Apply a function to each timeseries and append the results

        `func` is called like `func(ar, *args, **kwargs)` for each :class:`ScmRun <scmdata.run.ScmRun>` ``ar``
        in this group. If the result of this function call is None, than it is
        excluded from the results.

        The results are appended together using :func:`run_append`. The function
        can change the size of the input :class:`ScmRun <scmdata.run.ScmRun>` as long as :func:`run_append`
        can be applied to all results.

        Examples
        --------
        .. code:: python

            >>> from scmdata import ScmRun
            >>> def multiply_by_2(arr):
            ...     variable = arr.get_unique_meta("variable", True)
            ...     if variable == "Surface Temperature":
            ...         return arr * 2
            ...     return arr
            ...

            >>> run = ScmRun(
            ...     data=[[1, 2], [3, 4]],
            ...     index=[2010, 2020],
            ...     columns={
            ...         "variable": ["Surface Temperature", "Carbon Uptake"],
            ...         "model": "model",
            ...         "scenario": "scenario",
            ...         "region": "World",
            ...         "unit": ["K", "GtC / yr"],
            ...     },
            ... )
            >>> run.timeseries().sort_index()
            time                                                2010-01-01  2020-01-01
            model region scenario unit     variable
            model World  scenario GtC / yr Carbon Uptake               2.0         4.0
                                  K        Surface Temperature         1.0         3.0

            >>> run.apply(multiply_by_2).timeseries().sort_index()
            time                                                2010-01-01  2020-01-01
            model region scenario unit     variable
            model World  scenario GtC / yr Carbon Uptake               2.0         4.0
                                  K        Surface Temperature         2.0         6.0

        Parameters
        ----------
        func : function
            Callable to apply to each timeseries.

        *args
            Positional arguments passed to `func`.

        **kwargs
            Used to call `func(ar, **kwargs)` for each array `ar`.

        Returns
        -------
        applied : :class:`ScmRun <scmdata.run.ScmRun>`
            The result of splitting, applying and combining this array.
        """
        return self.groupby(self.meta.columns).apply(func, *args, **kwargs)

    def get_meta_columns_except(self, *not_group: Iterable[str] | str) -> list[str]:
        """
        Get columns in meta except a set

        Parameters
        ----------
        not_group: str or list of str
            Columns to exclude from the grouping

        Returns
        -------
        list
            Meta columns except the ones supplied (sorted alphabetically)
        """
        not_group = self._check_groupby_input(not_group)
        group = sorted(tuple(set(self.meta.columns) - set(not_group)))

        return group

    def groupby_all_except(self, *not_group: str) -> RunGroupBy[Self]:
        """
        Group the object by unique metadata apart from the input columns

        In other words, the groups are determined by all columns in
        ``self.meta`` except for  those in ``not_group``

        Parameters
        ----------
        not_group: str or list of str
            Columns to exclude from the grouping

        Returns
        -------
        :class:`RunGroupBy`
            See the documentation for :class:`RunGroupBy` for more information
        """
        from .groupby import RunGroupBy

        group = self.get_meta_columns_except(not_group)

        return RunGroupBy(self, group)

    def convert_unit(
        self,
        unit: str,
        context: str | None = None,
        inplace: bool = False,
        **kwargs: Any,
    ) -> Self:
        """
        Convert the units of a selection of timeseries.

        Uses :class:`scmdata.units.UnitConverter` to perform the conversion.

        Parameters
        ----------
        unit
            Unit to convert to. This must be recognised by
            :class:`~openscm.units.UnitConverter`.

        context
            Context to use for the conversion i.e. which metric to apply when performing
            CO2-equivalent calculations. If ``None``, no metric will be applied and
            CO2-equivalent calculations will raise :class:`DimensionalityError`.

        inplace
            If True, apply the conversion inplace, otherwise a copy is performed.

        **kwargs
            Extra arguments which are passed to :meth:`~ScmRun.filter` to
            limit the timeseries which are attempted to be converted. Defaults to
            selecting the entire ScmRun, which will likely fail.

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            A :class:`ScmRun <scmdata.run.ScmRun>` object containing converted units.

        Notes
        -----
        If ``context`` is not ``None``, then the context used for the conversion will
        be checked against any existing metadata and, if the conversion is valid,
        stored in the output's metadata.

        Raises
        ------
        ValueError
            ``"unit_context"`` is already included in ``self``'s :meth:`meta_attributes`
            and it does not match ``context`` for the variables to be converted.
        """
        ret = _get_target(self, inplace)

        to_convert_filtered = ret.filter(**kwargs, log_if_empty=False)
        to_not_convert_filtered = ret.filter(**kwargs, keep=False, log_if_empty=False)

        already_correct_unit = to_convert_filtered.filter(unit=unit, log_if_empty=False)
        if (
            "unit_context" in already_correct_unit.meta_attributes
            and not already_correct_unit.empty
        ):
            self._check_unit_context(already_correct_unit, context)

        to_convert = to_convert_filtered.filter(
            unit=unit, log_if_empty=False, keep=False
        )
        to_not_convert: Self = run_append(
            [to_not_convert_filtered, already_correct_unit]
        )

        if "unit_context" in to_convert.meta_attributes and not to_convert.empty:
            self._check_unit_context(to_convert, context)

        if context is not None:
            to_convert["unit_context"] = context

        if "unit_context" not in to_not_convert.meta_attributes and context is not None:
            to_not_convert["unit_context"] = None

        def apply_units(group):
            orig_unit = group.get_unique_meta("unit", no_duplicates=True)
            uc = UnitConverter(orig_unit, unit, context=context)

            group._df.values[:] = uc.convert_from(group._df.values)
            group["unit"] = unit

            return group

        ret = to_convert
        if not to_convert.empty:
            ret = ret.groupby("unit").apply(apply_units)

        ret = run_append([ret, to_not_convert], inplace=inplace)

        return ret

    @staticmethod
    def _check_unit_context(dat, context):
        unit_context = dat.get_unique_meta("unit_context")

        # check if contexts don't match, unless the context is nan
        non_matching_contexts = len(unit_context) > 1 or unit_context[0] != context
        if isinstance(unit_context[0], float):
            non_matching_contexts &= not np.isnan(unit_context[0])

        if non_matching_contexts:
            raise ValueError(
                f"Existing unit conversion context(s), `{unit_context}`, doesn't match input "
                f"context, `{context}`, drop `unit_context` metadata before doing "
                "conversion"
            )

    def relative_to_ref_period_mean(self, append_str=None, **kwargs):
        """
        Return the timeseries relative to a given reference period mean.

        The reference period mean is subtracted from all values in the input timeseries.

        Parameters
        ----------
        append_str
            Deprecated

        **kwargs
            Arguments to pass to :func:`filter` to determine the data to be included in
            the reference time period. See the docs of :func:`filter` for valid options.

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            New object containing the timeseries, adjusted to the reference period mean.
            The reference period year bounds are stored in the meta columns
            ``"reference_period_start_year"`` and ``"reference_period_end_year"``.

        Raises
        ------
        NotImplementedError
            ``append_str`` is not ``None``
        """
        if append_str is not None:
            raise NotImplementedError("`append_str` is deprecated")

        ts = self.timeseries()
        # mypy confused by `inplace` default
        ref_data = self.filter(**kwargs)
        ref_period_mean = ref_data.timeseries().mean(axis="columns")

        res = ts.sub(ref_period_mean, axis="index")
        res.reset_index(inplace=True)

        res["reference_period_start_year"] = ref_data["year"].min()
        res["reference_period_end_year"] = ref_data["year"].max()

        return type(self)(res)

    def append(
        self,
        other: GenericRun,
        inplace: bool = False,
        duplicate_msg: str | bool = True,
        metadata: MetadataType | None = None,
        **kwargs: Any,
    ) -> Self:
        """
        Append additional data to the current data.

        For details, see :func:`run_append`.

        Parameters
        ----------
        other
            Data (in format which can be cast to :class:`ScmRun <scmdata.run.ScmRun>`) to
             append.

        inplace
            If ``True``, append data in place, modifying the current object. Otherwise,
            a new :class:`ScmRun <scmdata.run.ScmRun>` instance is created.

        duplicate_msg
            If ``True``, raise a :class:`scmdata.errors.NonUniqueMetadataError` error
            so the user can see the duplicate timeseries. If ``False``, take the average
            and do not raise a warning or error. If ``"warn"``, raise a
            warning if duplicate data is detected.

        metadata
            If not ``None``, override the metadata of the resulting :class:`ScmRun <scmdata.run.ScmRun>` with
            ``metadata``. Otherwise, the metadata for the runs are merged. In the case
            where there are duplicate metadata keys, the values from the first run are
            used.

        **kwargs
            Keywords to pass to :func:`ScmRun.__init__` when reading
            :obj:`other`

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            Object containing the results of appending the timeseries in ``other``.

        Raises
        ------
        NonUniqueMetadataError
            If the appending results in timeseries with duplicate metadata and
            :attr:`duplicate_msg` is ``True``

        """
        if not isinstance(other, BaseScmRun):
            other = self.__class__(other, **kwargs)  # type: ignore

        return run_append(
            cast(Sequence[Self], (self, other)),
            inplace=inplace,
            duplicate_msg=duplicate_msg,
            metadata=metadata,
        )

    def append_timewise(
        self,
        other,
        align_columns,
    ):
        """
        Append timeseries along the time axis

        Parameters
        ----------
        other : :obj:`scmdata.ScmRun`
            :obj:`scmdata.ScmRun` containing the timeseries to append

        align_columns : list
            Columns used to align ``other`` and ``self`` when joining

        Returns
        -------
        :obj:`scmdata.ScmRun`
            Result of joining ``self`` and ``other`` along the time axis
        """
        ts_self = self.timeseries()
        try:
            ts_other = other.timeseries(meta=align_columns)
        except NonUniqueMetadataError as exc:
            error_msg = (
                "Calling ``other.timeseries(meta=align_columns)`` must "
                "result in umabiguous timeseries"
            )
            raise ValueError(error_msg) from exc

        ts_other_aligned, ts_self_aligned = ts_other.align(ts_self)
        ts_self_aligned = ts_self_aligned.dropna(how="all", axis="columns")
        ts_other_aligned = ts_other_aligned.dropna(how="all", axis="columns")

        # if ts_other_aligned.isna().any(axis=1):
        #     warning?

        out = pd.concat([ts_other_aligned, ts_self_aligned], axis=1)

        try:
            return type(self)(out)
        except DuplicateTimesError as exc:
            raise ValueError("``self`` and ``other`` have overlapping times") from exc

    def to_iamdataframe(self) -> LongDatetimeIamDataFrame:  # pragma: no cover
        """
        Convert to a :class:`LongDatetimeIamDataFrame` instance.

        :class:`LongDatetimeIamDataFrame` is a subclass of :class:`pyam.IamDataFrame`.
        We use :class:`LongDatetimeIamDataFrame` to ensure all times can be handled, see
        docstring of :class:`LongDatetimeIamDataFrame` for details.

        Returns
        -------
        :class:`LongDatetimeIamDataFrame`
            :class:`LongDatetimeIamDataFrame` instance containing the same data.

        Raises
        ------
        ImportError
            If `pyam <https://github.com/IAMconsortium/pyam>`_ is not installed
        """
        # Lazy load
        from .pyam_compat import LongDatetimeIamDataFrame

        if LongDatetimeIamDataFrame is None:
            raise ImportError(
                "pyam is not installed. Features involving IamDataFrame are unavailable"
            )

        return LongDatetimeIamDataFrame(self.timeseries())

    def to_csv(self, fname: FilePath, **kwargs: Any) -> None:
        """
        Write timeseries data to a csv file

        Parameters
        ----------
        fname
            Path to write the file into
        """
        self.timeseries().reset_index().to_csv(fname, **kwargs, index=False)

    def reduce(self, func, dim=None, axis=None, **kwargs):
        """
        Apply a function along a given axis

        This is to provide the GroupBy functionality in :func:`ScmRun.groupby` and is
        not generally called directly.

        This implementation is very bare-bones - no reduction along the time time
        dimension is allowed and only the `dim` parameter is used.

        Parameters
        ----------
        func: function
        dim : str
            Ignored
        axis : int
            The dimension along which the function is applied. The only valid value is 0
            which corresponds to the along the time-series dimension.
        kwargs
            Other parameters passed to `func`

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`

        Raises
        ------
        ValueError
            If a dimension other than None is provided

        NotImplementedError
            If `axis` is anything other than 0
        """
        if dim is not None:
            raise ValueError("ScmRun.reduce does not handle dim. Use axis instead")

        input_data = self.values

        if axis is None or axis == 1:
            raise NotImplementedError(
                "Cannot currently reduce along the time dimension"
            )

        if axis is not None:
            data = func(input_data, axis=axis, **kwargs)
        else:
            data = func(input_data, **kwargs)

        if getattr(data, "shape", ()) == self.shape:
            return type(self)(
                data,
                index=self.time_points,
                columns=cast(
                    dict[str, MetadataValue | Iterable[MetadataValue]],
                    self.meta.to_dict("list"),
                ),
            )
        else:
            removed_axes = range(2) if axis is None else np.atleast_1d(axis) % 2
            index = self.time_points
            meta = self.meta.to_dict("list")
            if 0 in removed_axes and len(meta):
                # Reduced the timeseries
                m = self.meta
                n_unique = m.nunique(axis=0)
                m = m.drop(columns=n_unique[n_unique > 1].index).drop_duplicates()
                if len(m) != 1:  # pragma: no cover
                    raise AssertionError(m)

                meta: dict[str, MetadataValue | Iterable[MetadataValue]] = m.to_dict(  # type: ignore
                    "list"
                )

            if 1 in removed_axes:
                raise NotImplementedError  # pragma: no cover

            return type(self)(data, index=index, columns=meta)

    def round(self, decimals: int = 3, inplace: bool = False) -> Self:
        """
        Round data to a given number of decimal places.

        For values exactly halfway between rounded decimal values, NumPy rounds
        to the nearest even value. Thus 1.5 and 2.5 round to 2.0, -0.5 and 0.5
        round to 0.0, etc.

        Parameters
        ----------
        decimals : int
            Number of decimal places to round each value to.

        inplace : bool
            If True, apply the conversion inplace, otherwise a copy is performed.

        Returns
        -------
        :class:`ScmRun <scmdata.run.ScmRun>`
            :class:`ScmRun <scmdata.run.ScmRun>` containing the rounded values.

        """
        ret = _get_target(self, inplace)

        # Check if any values are smaller than half the smallest step
        # They may be rounded down to zero
        min_value = ret._df.abs().min().min()
        if min_value <= 0.5 * 10**-decimals:
            warnings.warn(
                "There are small values which may be truncated during rounding. Either increase the number"
                "of decimals or convert the units of the timeseries so that the quantities are larger."
            )

        ret._df = ret._df.round(decimals)

        return ret


def _merge_metadata(metadata):
    res = metadata[0].copy()

    for m in metadata[1:]:
        for k, v in m.items():
            if k not in res:
                res[k] = v
    return res


def run_append(  # noqa: PLR0912, PLR0915
    runs: Sequence[GenericRun | pd.DataFrame],
    inplace: bool = False,
    duplicate_msg: str | bool = True,
    metadata: MetadataType | None = None,
) -> GenericRun:
    """
    Append together many objects.

    When appending many objects, it may be more efficient to call this routine once with
    a list of :class:`ScmRun <scmdata.run.ScmRun>`'s, than using :func:`ScmRun.append` multiple times.

    Parameters
    ----------
    runs: list of :class:`ScmRun <scmdata.run.ScmRun>` or :class:`pd.DataFrame`
        The runs to append. Values will be attempted to be cast to :class:`ScmRun <scmdata.run.ScmRun>`.

    inplace
        If ``True``, then the operation updates the first item in :obj:`runs` inplace.
        Otherwise, the results are appended to a new object.

    duplicate_msg
        If ``True``, raise a ``NonUniqueMetadataError`` error so the user can
        see the duplicate timeseries. If ``False``, take the average and do
        not raise a warning or error. If ``"warn"``, raise a warning if
        duplicate data is detected.

    metadata
        If not ``None``, override the metadata of the resulting :class:`ScmRun <scmdata.run.ScmRun>` with
        ``metadata``. Otherwise, the metadata for the runs are merged. In the case where
        there are duplicate metadata keys, the values from the first run are used.

    Returns
    -------
    :class:`ScmRun <scmdata.run.ScmRun>`
        Object containing the appended data. The resultant class will be determined by
        the type of the first object.

    Raises
    ------
    TypeError
        If :obj:`inplace` is ``True`` but the first element in :obj:`dfs` is not an
        instance of :class:`ScmRun <scmdata.run.ScmRun>`

        ``runs`` argument is not a list

    ValueError
        :obj:`duplicate_msg` option is not recognised.

        No runs are provided to be appended
    """
    if not isinstance(runs, Sequence):
        raise TypeError("runs is not a list")

    if not len(runs):
        raise ValueError("No runs to append")

    if inplace:
        if not isinstance(runs[0], BaseScmRun):
            raise TypeError("Can only append inplace to an ScmRun")
        ret: GenericRun = cast(GenericRun, runs[0])
    elif isinstance(runs[0], pd.DataFrame):
        ret = scmdata.ScmRun(runs[0])  # type: ignore
    else:
        ret = runs[0].copy()

    to_join_dfs: list[pd.DataFrame] = []
    to_join_metas = []
    overlapping_times = False

    return_index = pd.Index(range(ret._df.shape[1]))
    ret._df.columns = return_index
    ret._meta.index = return_index

    min_idx = ret._df.shape[1]
    for run in runs[1:]:
        if isinstance(run, pd.DataFrame):
            run_to_join_df: pd.DataFrame = run.T
            run_to_join_meta: pd.DataFrame = run.index.to_frame()
        else:
            run_to_join_df = run._df
            run_to_join_meta = run._meta.to_frame()

        max_idx = min_idx + run_to_join_df.shape[1]
        new_index = pd.Index(range(min_idx, max_idx))
        min_idx = max_idx

        run_to_join_df.columns = new_index
        run_to_join_meta.index = new_index

        # check everything still makes sense
        npt.assert_array_equal(run_to_join_meta.index, run_to_join_df.columns)

        # check for overlap
        idx_to_check = run_to_join_df.index
        if not overlapping_times and (
            idx_to_check.isin(ret._df.index).any()
            or any([idx_to_check.isin(df.index).any() for df in to_join_dfs])
        ):
            overlapping_times = True

        to_join_dfs.append(run_to_join_df)
        to_join_metas.append(run_to_join_meta)

    ret._df = pd.concat([ret._df, *to_join_dfs], axis="columns").sort_index()
    ret._time_points = TimePoints(ret._df.index.values)
    ret._df.index = ret._time_points.to_index()
    if not all(m.empty for m in to_join_metas):
        ret._meta = pd.MultiIndex.from_frame(
            pd.concat([ret._meta.to_frame(), *to_join_metas]).astype("category")
        )

    if ret._duplicated_meta():
        if overlapping_times and duplicate_msg:
            _handle_potential_duplicates_in_append(ret, duplicate_msg)

        ts = ret.timeseries(check_duplicated=False)
        orig_ts_index = ts.index
        nan_cols = pd.isna(orig_ts_index.to_frame()).any()
        orig_dtypes = orig_ts_index.to_frame().dtypes

        # Convert index to str
        ts.index = pd.MultiIndex.from_frame(
            ts.index.to_frame().astype(str).reset_index(drop=True)
        )

        deduped_ts = ts.groupby(ts.index, as_index=True).mean()

        ret._df = deduped_ts.reset_index(drop=True).T

        new_meta = pd.DataFrame.from_records(
            deduped_ts.index.values, columns=ts.index.names
        )

        # Convert back from str
        for c in nan_cols[nan_cols].index:
            new_meta[c].replace("nan", np.nan, inplace=True)
        for c, dtype in orig_dtypes.items():
            new_meta[c] = new_meta[c].astype(dtype)

        ret._meta = pd.MultiIndex.from_frame(new_meta.astype("category"))

    if metadata is not None:
        ret.metadata = metadata
    else:
        ret.metadata = _merge_metadata(
            [r.metadata if hasattr(r, "metadata") else {} for r in runs]
        )
    return ret


def _handle_potential_duplicates_in_append(data, duplicate_msg):
    if duplicate_msg == "warn":
        warn_msg = (
            "Duplicate time points detected, the output will be the average of "
            "the duplicates.  Set `duplicate_msg=False` to silence this message."
        )
        warnings.warn(warn_msg)
        return None

    if duplicate_msg and not isinstance(duplicate_msg, str):
        raise NonUniqueMetadataError(data.meta)

    raise ValueError("Unrecognised value for duplicate_msg")


inject_nc_methods(BaseScmRun)
inject_plotting_methods(BaseScmRun)
inject_ops_methods(BaseScmRun)
inject_xarray_methods(BaseScmRun)


class ScmRun(BaseScmRun):
    """
    Data container for holding one or many time-series of SCM data.
    """

    required_cols: tuple[str, ...] = ("model", "scenario", "region", "variable", "unit")
    """
    Minimum metadata columns required by an ScmRun.

    If an application requires a different set of required metadata, this
    can be specified by overriding :attr:`required_cols` on a custom class
    inheriting :class:`scmdata.run.BaseScmRun`. Note that at a minimum,
    ("variable", "unit") columns are required.
    """
