"""
This module constains a set of functions dadicated to plot
trajectories and extracted statistical data from ``yupi.stats``.

All the resources of this module should be imported directly
from ``yupi.graphics``.
"""

from yupi.graphics._stats_plots import (
    plot_angles_hist,
    plot_hist,
    plot_hists,
    plot_kurtosis,
    plot_msd,
    plot_psd,
    plot_speed_hist,
    plot_vacf,
)
from yupi.graphics._style import DOTTED, LINE, LINE_DOTTED
from yupi.graphics._trajs_plots import plot_2d, plot_3d, plot_vs_time

__all__ = [
    "DOTTED",
    "LINE",
    "LINE_DOTTED",
    "plot_2d",
    "plot_3d",
    "plot_angles_hist",
    "plot_hist",
    "plot_hists",
    "plot_kurtosis",
    "plot_msd",
    "plot_psd",
    "plot_speed_hist",
    "plot_vacf",
    "plot_vs_time",
]
