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
    # 1. Generate dummy data & compute homology
    # data = np.random.random((100, 2))



    df = pd.read_csv(data)

    data_array = df.to_numpy()
    diagrams = ripser(data_array)['dgms']

    # 2. Extract H0 and H1 diagrams
    # (Replacing infinity values with a readable cap for plotting)
    dgm0 = diagrams[0]
    dgm1 = diagrams[1]

    # Cap infinity values for H0 visibility
    max_finite = max([p[1] for p in dgm1 if p[1] != np.inf] + [p[1] for p in dgm0 if p[1] != np.inf])
    dgm0[dgm0 == np.inf] = max_finite * 1.2 

    # 2. Initialize the fig and ax objects
    fig, ax = plt.subplots(figsize=(5, 5))

    # 3. Plot H0 bars
    for i, (birth, death) in enumerate(dgm0):
        ax.hlines(y=i, xmin=birth, xmax=death, colors='red', linewidth=2, label='$H_0$' if i == 0 else "")

    # 4. Plot H1 bars (stacked above H0)
    h0_count = len(dgm0)
    for i, (birth, death) in enumerate(dgm1):
        ax.hlines(y=h0_count + i, xmin=birth, xmax=death, colors='blue', linewidth=2, label='$H_1$' if i == 0 else "")

    # 5. Customize using ax methods
    ax.set_title("Persistence Barcode")
    ax.set_xlabel("Filtration Value ($\epsilon$)")
    ax.set_ylabel("Topological Features")
    ax.grid(axis='x', linestyle='--')
    ax.legend()

    plt.tight_layout()
    plt.show()

    # df = pd.read_csv(data)

    # data_array = df.to_numpy()

    


    # result = ripser(data_array)
    # dgms = result['dgms']
    # print(dgms)

    # fig, ax = plt.subplots(figsize=(5, 5))
    # plot_diagrams(dgms, plot_type='barcode')


    # plot_diagrams(dgms, ax=ax)

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

# # 1. Generate data (using a circle to ensure features exist)
# # t = np.linspace(0, 2*np.pi, 100)
# # data = np.c_[np.cos(t), np.sin(t)] + 0.1 * np.random.randn(100, 2)

# # 2. Compute diagrams
# result = ripser(data)
# dgms = result['dgms']

# # 3. Validation: Print types to debug
# print(f"Diagrams type: {type(dgms)}")
# for i, d in enumerate(dgms):
#     print(f"H{i} shape: {d.shape}")

# # 4. Plotting
# plt.figure(figsize=(5,5))
# plot_diagrams(dgms, show=True)

# print(dgms)

