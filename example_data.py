

# Imports
import numpy as np
import plotly.graph_objects as go

import json



# 3D circle (ring) data set
def S1() :

    num_points = 75
    theta = np.linspace(0, 2 * np.pi, num_points)
    radius = 2.0

    x = radius * np.cos(theta) 
    y = radius * np.sin(theta) 
    z = np.zeros(num_points) 

    return (x,y,z,theta)

# 3D circle (ring) data set with noise
def noisy_S1() :

    
    num_points = 1000
    theta = np.linspace(0, 2 * np.pi, num_points)
    radius = 2.0

    x = radius * np.cos(theta) + np.random.normal(0, 0.15, num_points)
    y = radius * np.sin(theta) + np.random.normal(0, 0.15, num_points)
    z = np.zeros(num_points) + np.random.normal(0, 0.15, num_points)

    return (x,y,z,theta)


# 3D 2-sphere data set
def S2():

    num_points = 500
    radius = 2.0

    # Generate points uniformly distributed across a sphere's surface
    # Using random sampling prevents the points from clustering tightly at the poles
    phi = np.random.uniform(0, 2 * np.pi, num_points)       # Longitudinal angle
    costheta = np.random.uniform(-1, 1, num_points)         # Latitudinal distribution
    theta = np.arccos(costheta)

    # 2. Convert spherical coordinates to Cartesian 3D coordinates (x, y, z)
    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(theta)

    return (x, y, z,phi)


# mapping the color to theta will color the donut in rings wrapping around the tube, while
# mapping the color to phi will color it in wedge slices around the main ring.
def Torus(num_points=750, R=2.0, r=.75):
    """
    Generates a 3D point cloud of a torus (S1 x S1).
    R: Major radius (distance from the center of the tube to the center of the torus)
    r: Minor radius (radius of the tube itself)
    """
    # 1. Generate two independent uniform angles from 0 to 2*pi
    # theta spins around the inner tube (the first S1)
    theta = np.random.uniform(0, 2 * np.pi, num_points)
    # phi spins around the center origin of the whole ring (the second S1)
    phi = np.random.uniform(0, 2 * np.pi, num_points)

    # 2. Parametric equations for a torus
    x = (R + r * np.cos(theta)) * np.cos(phi)
    y = (R + r * np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)

    return (x, y, z,phi)

# When you pass this data into your Plotly setup, try setting
# the marker color to the original t array (color=t). The color
# gradient will beautifully flow from one end of the infinity symbol
# all the way through the loop paths to the other side.
def InfinitySymbol(num_points=1500, scale=2.0):
    """
    Generates a 3D point cloud of a figure-eight infinity symbol.
    scale: Adjusts the overall width of the loops.
    """
    # 1. Generate parameter t from 0 to 2*pi to complete a full double loop
    t = np.linspace(0, 2 * np.pi, num_points)

    # 2. Parametric equations for the figure-eight layout
    # x traces a back-and-forth motion twice as fast as y, creating the crossover
    x = scale * np.sin(t)
    y = scale * np.sin(t) * np.cos(t) # Equivalent to: 0.5 * scale * np.sin(2*t)
    
    # 3. Add a slight 3D wave in the Z-axis so it loops over/under itself at the center
    # If you prefer a completely flat 2D symbol, change this to np.zeros(num_points)
    z = (scale * 0.2) * np.sin(2 * t)

    # 4. Optional: Add a tiny touch of random sensor noise for realism
    x += np.random.normal(0, 0.05, num_points)
    y += np.random.normal(0, 0.05, num_points)
    z += np.random.normal(0, 0.05, num_points)

    return (x, y, z)






def InfinityTube(num_backbone_points=100, num_tube_points=40, scale=2.0, tube_radius=0.4):
    """
    Generates a thick 3D tube following a figure-eight infinity path with no noise.
    
    num_backbone_points: How many slices along the infinity loop.
    num_tube_points: How many points make up the circular ring of each slice.
    scale: Width of the infinity loops.
    tube_radius: Thickness of the pipe.
    """
    # 1. Setup the tracking parameters
    t = np.linspace(0, 2 * np.pi, num_backbone_points)
    theta = np.linspace(0, 2 * np.pi, num_tube_points)
    
    # Pre-allocate arrays to hold the final coordinate cloud
    total_points = num_backbone_points * num_tube_points
    x_out = np.zeros(total_points)
    y_out = np.zeros(total_points)
    z_out = np.zeros(total_points)
    
    idx = 0
    for i in range(num_backbone_points):
        # 2. Calculate the backbone point position at time t[i]
        bx = scale * np.sin(t[i])
        by = scale * np.sin(t[i]) * np.cos(t[i])
        bz = (scale * 0.2) * np.sin(2 * t[i])
        
        # 3. Calculate the tangent vector (the direction the curve is moving)
        # We find this by taking the mathematical derivative of the backbone equations
        tx = scale * np.cos(t[i])
        ty = scale * (np.cos(t[i])**2 - np.sin(t[i])**2)
        tz = 2 * (scale * 0.2) * np.cos(2 * t[i])
        
        tangent = np.array([tx, ty, tz])
        tangent /= np.linalg.norm(tangent) # Normalize to length 1
        
        # 4. Create a coordinate frame perpendicular to the moving direction
        # We pick an arbitrary up vector to find the first perpendicular vector (normal)
        up = np.array([0, 0, 1]) if abs(tangent[2]) < 0.9 else np.array([0, 1, 0])
        normal = np.cross(tangent, up)
        normal /= np.linalg.norm(normal)
        
        # Find the second perpendicular vector (binormal) to complete the 3D cross
        binormal = np.cross(tangent, normal)
        
        # 5. Sweep a circle around the backbone point using the normal vectors
        for j in range(num_tube_points):
            # Calculate the offset circle using torus-like math
            circle_x = tube_radius * np.cos(theta[j])
            circle_y = tube_radius * np.sin(theta[j])
            
            # Project the flat circle into 3D space aligned with the tube direction
            x_out[idx] = bx + circle_x * normal[0] + circle_y * binormal[0]
            y_out[idx] = by + circle_x * normal[1] + circle_y * binormal[1]
            z_out[idx] = bz + circle_x * normal[2] + circle_y * binormal[2]
            idx += 1
            
    return x_out, y_out, z_out







def plot_data(data):
    
    
    # Create the figure
    fig = go.Figure()

    # 3. Add the Point Cloud trace
    fig.add_trace(go.Scatter3d(
        x=data[0], y=data[1], z=data[2],
        mode='markers',
        name='Point Cloud',
        hoverinfo='none', # Disables the tooltip popups completely
        # marker=dict(size=4, color=theta, colorscale='Viridis', opacity=0.8)
        # marker=dict(size=4, color=z, colorscale='Viridis', opacity=0.8)
        # marker=dict(size=4, color=data[0], colorscale='Jet', opacity=0.8)
        # marker=dict(size=4, color=data[2], colorscale='turbo', opacity=0.8)
        marker=dict(size=4, color=data[3], colorscale='turbo', opacity=0.8)
    ))


    # Define lines for the X, Y, and Z axes through the origin
    axis_range = [-2.5, 2.5]

    # X-axis line 
    fig.add_trace(go.Scatter3d(
        x=axis_range, y=[0, 0], z=[0, 0], 
        mode='lines', name='X Axis', line=dict(color='black', width=4)
    ))

    # Y-axis line
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=axis_range, z=[0, 0], 
        mode='lines', name='Y Axis', line=dict(color='black', width=4)
    ))

    #Z-axis line
    fig.add_trace(go.Scatter3d(
        # x=[0, 0], y=[0, 0], z=[-1, 1], 
        x=[0, 0], y=[0, 0], z=axis_range,
        mode='lines', name='Z Axis', line=dict(color='black', width=4)
    ))

    # Configure layout
    fig.update_layout(
        # title='Plotly 3D Circle with Center Axes Lines',
        scene=dict(
            xaxis=dict(title='X', range=[-2.5, 2.5], showspikes=False), # Turns off X projection lines
            yaxis=dict(title='Y', range=[-2.5, 2.5], showspikes=False), # Turns off Y projection lines
            # zaxis=dict(title='Z', range=[-1, 1], showspikes=False),    # Turns off Z projection lines
            zaxis=dict(title='Z', range=[-2.5, 2.5], showspikes=False),    # Turns off Z projection lines
            # aspectmode='data',
            aspectmode='cube',
            
            
        ),
        autosize=True,
        # margin=dict(l=0, r=0, b=0, t=40),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False, # Remove the sidebar legend
        hovermode=False, # Completely kills the hover detection system
    )

    return fig







data = Torus()
print(type(data))


arr = np.column_stack(data[:3])
print(len(arr))
print(arr.shape)
print(arr.size)

np.savetxt(
    "S1xS1.csv",
    arr,
    delimiter=",",
    fmt="%g"
)




# Call the function to get the figure object
# my_plot = plot_data(InfinityTube())
# my_plot = plot_data(Torus())
# my_plot = plot_data(noisy_S1())
my_plot = plot_data(data)

# Display 
my_plot.show()

# Save to interactive HTML file
# my_plot.write_html("500S2.html")
fig_json = my_plot.to_json()

with open("static/plots/S1xS1.json", "w") as f:
    f.write(fig_json)