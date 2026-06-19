import numpy as np
from ripser import ripser
from persim import plot_diagrams

import pandas as pd

import matplotlib
matplotlib.use("Agg") # insures non interactive display for server

import matplotlib.pyplot as plt
import io


# Check, sanatize, and validate data
def validate_data(data):
    return None

# Compute PH and create diagrams
def ph_diagram (data,dimension,prime,metric):

    df = pd.read_csv(data)

    data_array = df.to_numpy()

    result = ripser(data_array, coeff=prime, maxdim=dimension, metric=metric)
    dgms = result['dgms']
    # print(dgms)

    fig, ax = plt.subplots(figsize=(5, 5))
    plot_diagrams(dgms, ax=ax)

    
    buffer = io.BytesIO()

    fig.savefig(buffer, format="png")

    plt.close(fig)

    buffer.seek(0)

    return buffer
#########################################
## Barcode
########################################
def barcode(data, dimension, prime, metric):
    """
    Compute persistent homology using Ripser and generate persistence
    barcode plots.

    Parameters
    ----------
    data : str
        Path to CSV file containing point-cloud data.

    dimension : int
        Maximum homology dimension to compute.
            0 -> H0
            1 -> H0, H1
            2 -> H0, H1, H2

    prime : int
        Coefficient field prime (e.g. 2, 3, 5).

    metric : str
        Metric used by Ripser (e.g. 'euclidean').

    Returns
    -------
    io.BytesIO
        PNG image buffer containing the barcode plot.
    """

    # ---------------------------------------------------------
    # 1. Load data
    # ---------------------------------------------------------
    df = pd.read_csv(data)
    data_array = df.to_numpy()

    # ---------------------------------------------------------
    # 2. Compute persistent homology
    # ---------------------------------------------------------
    diagrams = ripser(
        data_array,
        coeff=prime,
        maxdim=dimension,
        metric=metric
    )["dgms"]

    # diagrams[0] = H0
    # diagrams[1] = H1 (if dimension >= 1)
    # diagrams[2] = H2 (if dimension >= 2)

    # ---------------------------------------------------------
    # 3. Determine persistence threshold
    # ---------------------------------------------------------
    # Collect lifetimes from every homology group.
    # Ignore infinite bars when computing persistence statistics.
    # ---------------------------------------------------------
    all_finite_lifetimes = []

    for dgm in diagrams:
        for birth, death in dgm:
            if death != np.inf:
                all_finite_lifetimes.append(death - birth)

    max_persistence = (
        max(all_finite_lifetimes)
        if all_finite_lifetimes
        else 1.0
    )

    threshold_percentage = 0.10
    min_persistence = max_persistence * threshold_percentage

    # ---------------------------------------------------------
    # 4. Filter diagrams
    # ---------------------------------------------------------
    filtered_diagrams = []

    for dgm in diagrams:
        filtered = [
            p for p in dgm
            if (p[1] - p[0]) >= min_persistence
            or p[1] == np.inf
        ]
        filtered_diagrams.append(filtered)

    # ---------------------------------------------------------
    # 5. Find a cap value for infinite bars
    # ---------------------------------------------------------
    all_finite_deaths = []

    for dgm in filtered_diagrams:
        for birth, death in dgm:
            if death != np.inf:
                all_finite_deaths.append(death)

    max_finite = (
        max(all_finite_deaths)
        if all_finite_deaths
        else 1.0
    )

    infinity_cap = max_finite * 1.2

    # ---------------------------------------------------------
    # 6. Replace infinite deaths with cap value
    # ---------------------------------------------------------
    processed_diagrams = []

    for dgm in filtered_diagrams:

        processed = []

        for birth, death in dgm:

            if death == np.inf:
                processed.append([birth, infinity_cap])
            else:
                processed.append([birth, death])

        processed.sort(key=lambda x: x[0])

        processed_diagrams.append(processed)

    # ---------------------------------------------------------
    # 7. Create dynamic number of subplots
    # ---------------------------------------------------------
    n_groups = len(processed_diagrams)

    fig_height = 3 * n_groups

    fig, axes = plt.subplots(
        nrows=n_groups,
        ncols=1,
        figsize=(5, fig_height),
        sharex=True
    )

    # Special case:
    # When dimension=0, plt.subplots returns a single axis
    if n_groups == 1:
        axes = [axes]

    # colors = ["red", "blue", "green", "purple", "orange"]

    # ---------------------------------------------------------
    # 8. Plot each homology dimension
    # ---------------------------------------------------------
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    
    for dim, (ax, dgm) in enumerate(zip(axes, processed_diagrams)):

        color = default_colors[dim % len(default_colors)]

        for i, (birth, death) in enumerate(dgm):

            ax.hlines(
                y=i,
                xmin=birth,
                xmax=death,
                colors=color,
                linewidth=2
            )

        ax.set_ylabel(
            f"$H_{dim}$",
            rotation=0,
            labelpad=15,
            fontsize=12,
            fontweight="bold"
        )

        ax.set_ylim(
            -1,
            max(len(dgm) + 1, 8)
        )

        ax.get_yaxis().set_ticks([])

        ax.grid(
            axis="x",
            linestyle="--",
            alpha=0.7
        )

    # ---------------------------------------------------------
    # 9. Global plot formatting
    # ---------------------------------------------------------
    axes[-1].set_xlabel(
        r"Filtration Value ($\epsilon$)"
    )

    fig.suptitle(
        f"Persistence Barcode (Filtered < {threshold_percentage*100:.0f}%)",
        y=0.98
    )

    plt.subplots_adjust(hspace=0.15)

    plt.tight_layout()

    # ---------------------------------------------------------
    # 10. Save figure to memory buffer
    # ---------------------------------------------------------
    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        bbox_inches="tight"
    )

    plt.close(fig)

    buffer.seek(0)

    return buffer



