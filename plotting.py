
"""
Plotting utilities for the GEFS spread-error project.
"""

from pathlib import Path

import matplotlib.pyplot as plt


def plot_spread_rmse_by_lead(results_df, output_path=None):
    """
    Plot CONUS-mean ensemble spread and RMSE versus forecast lead time.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        results_df["forecast_hour"],
        results_df["spread_mean"],
        marker="o",
        label="Ensemble spread",
    )

    ax.plot(
        results_df["forecast_hour"],
        results_df["rmse"],
        marker="o",
        label="RMSE",
    )

    ax.set_xlabel("Forecast lead time (hours)")
    ax.set_ylabel("Temperature (K)")
    ax.set_title("GEFS 2-m Temperature Spread and RMSE by Lead Time")
    ax.grid(True, alpha=0.3)
    ax.legend()

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")

    return fig, ax


def plot_spread_error_scatter(results_by_fhr, output_path=None):
    """
    Make a scatter plot using all grid points from all forecast lead times.

    x-axis: ensemble spread
    y-axis: absolute forecast error
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    for fhr, data in results_by_fhr.items():
        spread = data["spread"].values.ravel()
        abs_error = abs(data["error"]).values.ravel()

        ax.scatter(
            spread,
            abs_error,
            s=3,
            alpha=0.2,
            label=f"f{fhr:03d}",
        )

    ax.set_xlabel("Ensemble spread (K)")
    ax.set_ylabel("Absolute forecast error (K)")
    ax.set_title("GEFS Spread vs. Absolute Error")
    ax.grid(True, alpha=0.3)
    ax.legend(markerscale=3)

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")

    return fig, ax
