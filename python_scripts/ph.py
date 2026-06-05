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
def ph_diagram (data):


    # print(type(data))
    # print(data)

    df = pd.read_csv(data)

    data_array = df.to_numpy()

    # print(type(data_array))
    # print("shape:" + str(data_array.shape))
    # print(data_array)


    result = ripser(data_array)
    dgms = result['dgms']
    print(dgms)

    fig, ax = plt.subplots(figsize=(5, 5))
    plot_diagrams(dgms, ax=ax)

    # plt.figure(figsize=(5,5))
    # plot_diagrams(dgms)
    # plot_diagrams(dgms, show=True)


    # 3. Plot the data as a barcode instead of a diagram
    # persim.plot_diagrams(diagrams, barcode=True)


    buffer = io.BytesIO()

    fig.savefig(buffer, format="png")

    plt.close(fig)

    buffer.seek(0)

    return buffer
#########################################
## Barcode
########################################
def barcode (data):

    df = pd.read_csv(data)

    data_array = df.to_numpy()
    
    diagrams = ripser(data_array)['dgms']

    # 2. Extract H0 and H1 diagrams
    # (Replacing infinity values with a readable cap for plotting)
    dgm0 = diagrams[0]
    dgm1 = diagrams[1]

        # 2. Dynamic threshold filtering
    all_finite_lifetimes = [(p[1] - p[0]) for dgm in [dgm0, dgm1] for p in dgm if p[1] != np.inf]
    max_persistence = max(all_finite_lifetimes) if all_finite_lifetimes else 1.0

    threshold_percentage = 0.10
    min_persistence = max_persistence * threshold_percentage

    filtered_dgm0 = [p for p in dgm0 if (p[1] - p[0]) >= min_persistence]
    filtered_dgm1 = [p for p in dgm1 if (p[1] - p[0]) >= min_persistence]

    # 3. Cap infinity values
    all_finite_deaths = [p[1] for p in filtered_dgm0 + filtered_dgm1 if p[1] != np.inf]
    max_finite = max(all_finite_deaths) if all_finite_deaths else 1.0
    filtered_dgm0 = [[p[0], max_finite * 1.2] if p[1] == np.inf else p for p in filtered_dgm0]

    filtered_dgm0.sort(key=lambda x: x[0])
    filtered_dgm1.sort(key=lambda x: x[0])

    # 4. Create vertically stacked plots sharing the X-axis
    # nrows=2 creates two subplots; sharex=True locks their horizontal scales together
    fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, figsize=(5, 6), sharex=True)

    # 5. Plot H0 Bars (Top Plot)
    for i, (birth, death) in enumerate(filtered_dgm0):
        ax0.hlines(y=i, xmin=birth, xmax=death, colors='red', linewidth=2)
    ax0.set_ylabel("$H_0$", rotation=0, labelpad=15, fontsize=12, fontweight='bold')
    ax0.set_ylim(-1, max(len(filtered_dgm0) + 1, 8)) # Keeps bars compressed
    ax0.get_yaxis().set_ticks([])                    # Hides numeric ticks
    ax0.grid(axis='x', linestyle='--')

    # 6. Plot H1 Bars (Bottom Plot)
    for i, (birth, death) in enumerate(filtered_dgm1):
        ax1.hlines(y=i, xmin=birth, xmax=death, colors='blue', linewidth=2)
    ax1.set_ylabel("$H_1$", rotation=0, labelpad=15, fontsize=12, fontweight='bold')
    ax1.set_ylim(-1, max(len(filtered_dgm1) + 1, 8)) # Keeps bars compressed
    ax1.get_yaxis().set_ticks([])                    # Hides numeric ticks
    ax1.grid(axis='x', linestyle='--')

    # 7. Global Layout Configurations
    ax1.set_xlabel("Filtration Value ($\epsilon$)")
    fig.suptitle(f"Persistence Barcode (Filtered < {threshold_percentage*100:.0f}%)", y=0.98)

    # Removes vertical whitespace gap between the two stacked plots
    plt.subplots_adjust(hspace=0.1)

    plt.tight_layout()
    # plt.show()



    buffer = io.BytesIO()

    fig.savefig(buffer, format="png")

    plt.close(fig)

    buffer.seek(0)

    return buffer



