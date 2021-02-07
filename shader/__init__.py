import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_datetime_or_timedelta_dtype


def find_runs(x: pd.Series) -> (np.ndarray, np.ndarray, np.ndarray):
    """Find runs of consecutive items in an array.
    From https://gist.github.com/alimanfoo/c5977e87111abe8127453b21204c1065."""

    # ensure array
    x = np.asanyarray(x)
    if x.ndim != 1:
        raise ValueError("only 1D array supported")
    n = x.shape[0]

    # handle empty array
    if n == 0:
        return np.array([]), np.array([]), np.array([])
    else:
        # find run starts
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])
        run_starts = np.nonzero(loc_run_start)[0]

        # find run values
        run_values = x[loc_run_start]

        # find run lengths
        run_lengths = np.diff(np.append(run_starts, n))

        return run_values, run_starts, run_lengths

def shade(
        series: pd.Series, ax: matplotlib.axes.Axes = None, start: int = 19, end: int = 7
):
    """Color dark phase in plot.
    Args:
    
        series (pd.Series) - Time-series variable
        ax (:class: `~matplotlib.axes.Axes`): axis to plot on (eg, `plt.gca()`)
        start (int): start of dark period/night
        end (hour): end of dark period/day
    Returns:

        ax (:class:`~matplotlib.axes._subplots.AxesSubplot`): Axes of plot
    """    
    assert is_datetime_or_timedelta_dtype(
        series.index
    ), f"Series must have datetime index but has {type(series.index)}"

    pd.plotting.register_matplotlib_converters() # prevents type error with axvspan

    if not ax:
        ax = plt.gca()

    # get boundaries for dark times
    dark_mask = (series.index.hour >= start) | (series.index.hour < end)
    run_values, run_starts, run_lengths = find_runs(dark_mask)
    for idx, is_dark in enumerate(run_values):
        if is_dark:
            start = run_starts[idx]
            end = run_starts[idx] + run_lengths[idx] - 1
            ax.axvspan(series.index[start], series.index[end], alpha=0.5, color="gray")
    
    fig = plt.gcf()
    fig.autofmt_xdate()
    return ax