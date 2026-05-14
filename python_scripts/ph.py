import numpy as np
from ripser import ripser
from persim import plot_diagrams

import matplotlib
matplotlib.use("Agg") # insures non interactive display for server

import matplotlib.pyplot as plt
import io


# Check, sanatize, and validate data
def validate_data(data):
    return None

# Compute PH and create diagrams
def ph_diagram (data):
    print(type(data))

    data_array = np.array(data)

    print(type(data_array))

    result = ripser(data_array)
    dgms = result['dgms']

    fig, ax = plt.subplots(figsize=(5, 5))
    plot_diagrams(dgms, ax=ax)

    # plt.figure(figsize=(5,5))
    # plot_diagrams(dgms)
    # plot_diagrams(dgms, show=True)


    buf = io.BytesIO()

    fig.savefig(buf, format="png")
    plt.close(fig)

    buf.seek(0)

    return buf
    

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

