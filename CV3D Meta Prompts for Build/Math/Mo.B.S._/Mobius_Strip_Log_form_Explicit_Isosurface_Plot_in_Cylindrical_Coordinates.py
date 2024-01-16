import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to calculate r
def calculate_r(theta, z):
    with np.errstate(divide='ignore', invalid='ignore'):
        r = np.exp(z * np.cos(theta / 2) / np.sin(theta / 2))
        r[np.isnan(r)] = 0
        r[np.isinf(r)] = 0
    return r

# Creating a grid of theta and z values
theta = np.linspace(0, 2 * np.pi, 100)
z = np.linspace(-10, 10, 100)
theta, z = np.meshgrid(theta, z)

# Calculating corresponding r values
r = calculate_r(theta, z)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Using the r values as color
color = np.log(r + 1)  # Adding 1 to avoid log(0), and using log to scale color values
color = (color - np.min(color)) / (np.max(color) - np.min(color))  # Normalizing

# Plotting theta, z, and using color to represent r
surf = ax.plot_surface(theta, z, r, facecolors=plt.cm.viridis(color))


ax.set_xlabel('Theta (radians)')
ax.set_ylabel('Z axis')
ax.set_zlabel('R axis')
plt.title('Plot in Cylindrical Polar Coordinates')

# Adding a color bar to represent the values of r
mappable = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=np.min(r), vmax=np.max(r)))
mappable.set_array(r)
plt.colorbar(mappable, ax=ax, label='r value')

plt.show()
