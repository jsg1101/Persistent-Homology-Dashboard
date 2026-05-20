import numpy as np
import plotly.graph_objects as go

# 1. Create a 3D circle (ring) data set
num_points = 500
theta = np.linspace(0, 2 * np.pi, num_points)

# Define circle geometry in the XY plane
radius = 5.0
x = radius * np.cos(theta)
y = radius * np.sin(theta)
# Keep Z constant at 0 for a flat circle, or add np.sin(theta*4) for a wavy ring
z = np.zeros(num_points) 

# Add random noise to simulate a real-world sensor point cloud
noise_level = 0.15
x += np.random.normal(0, noise_level, num_points)
y += np.random.normal(0, noise_level, num_points)
z += np.random.normal(0, noise_level, num_points)

# 2. Plot the point cloud with Plotly
fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=4,
        color=theta,          # Color points by angle to create a rainbow gradient
        colorscale='Viridis', # Beautiful built-in color scheme
        opacity=0.8
    )
)])

# 3. Configure the 3D scene layout
fig.update_layout(
    title='Plotly 3D Circle Point Cloud',
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
        # This keeps the aspect ratio square so the circle doesn't look like an oval
        aspectmode='data' 
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# 4. Launch the interactive browser plot
fig.show()
