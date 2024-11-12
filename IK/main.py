from functions import *
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

from IK_class import IKHandler
import asyncio
import websockets


##################################################
#                   2D arm 
##################################################

# Orientering = np.array([np.deg2rad(0.0), np.deg2rad(0.0)])

# r = 10
# s = 10

# # Function to update the plot
# def update(val):
#     angle1 = np.deg2rad(slider1.val)
#     angle2 = np.deg2rad(slider2.val)
#     x1 = r * np.cos(angle1)
#     y1 = r * np.sin(angle1)
#     x2 = x1 + s * np.cos(angle2)
#     y2 = y1 + s * np.sin(angle2)
    
#     arm.set_data([0, x1], [0, y1])
#     forearm.set_data([x1, x2], [y1, y2])
#     fig.canvas.draw_idle()


# # Create the plot
# fig, ax = plt.subplots()
# plt.subplots_adjust(left=0.1, bottom=0.3)

# x1 = r * np.cos(Orientering[0])
# y1 = r * np.sin(Orientering[0])
# x2 = x1 + s * np.cos(Orientering[1])
# y2 = y1 + s * np.sin(Orientering[1])

# arm, = plt.plot([0, x1], [0, y1], "ro-", label="arm")
# forearm, = plt.plot([x1, x2], [y1, y2], "bo-", label="forearm")

# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.axis('equal')

# plt.xlim([-30, 30])
# plt.ylim([-1, 30])

# # Create sliders
# axcolor = 'lightgoldenrodyellow'
# ax_slider1 = plt.axes([0.1, 0.2, 0.8, 0.03], facecolor=axcolor)
# ax_slider2 = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor)

# slider1 = Slider(ax_slider1, 'Angle 1', 0.0, 180.0, valinit=np.rad2deg(Orientering[0]))
# slider2 = Slider(ax_slider2, 'Angle 2', 0.0, 180.0, valinit=np.rad2deg(Orientering[1]))

# # Attach the update function to the sliders
# slider1.on_changed(update)
# slider2.on_changed(update)

# plt.show()


##################################################
#                   3D arm 
##################################################
# O = np.array([np.deg2rad(0), np.deg2rad(0), np.deg2rad(0)])

# r = 10 
# s = 10 

# # First point 
# x1 = r*np.cos(O[0])*np.sin(O[1])
# y1 = r*np.sin(O[0])*np.sin(O[1])
# z1 = r*np.cos(O[1])

# # Second point 
# x2 = x1+s*np.cos(O[0])*np.sin(O[2])
# y2 = y1+s*np.sin(O[0])*np.sin(O[2])
# z2 = z1+s*np.cos(O[2])

def set_equal_aspect_3d(ax):
    """Sets the aspect ratio for a 3D plot to be equal for all axes."""
    extents = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
    centers = np.mean(extents, axis=1)
    max_range = np.max(np.ptp(extents, axis=1)) / 2

    ax.set_xlim3d([centers[0] - max_range, centers[0] + max_range])
    ax.set_ylim3d([centers[1] - max_range, centers[1] + max_range])
    ax.set_zlim3d([centers[2] - max_range, centers[2] + max_range])

# # Function to update the plot
# def update(val):
#     angle1 = np.deg2rad(slider1.val)
#     angle2 = np.deg2rad(slider2.val)
#     angle3 = np.deg2rad(slider3.val)
    
#     x1 = r * np.cos(angle1) * np.sin(angle2)
#     y1 = r * np.sin(angle1) * np.sin(angle2)
#     z1 = r * np.cos(angle2)
    
#     x2 = x1 + s * np.cos(angle1) * np.sin(angle3)
#     y2 = y1 + s * np.sin(angle1) * np.sin(angle3)
#     z2 = z1 + s * np.cos(angle3)
    
#     arm.set_data([0, x1], [0, y1])
#     arm.set_3d_properties([0, z1])
    
#     forearm.set_data([x1, x2], [y1, y2])
#     forearm.set_3d_properties([z1, z2])
    
#     set_equal_aspect_3d(ax)
    
#     fig.canvas.draw_idle()

# # Create the plot with a larger figure size
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# plt.subplots_adjust(left=0.1, bottom=0.3)

# x1 = r * np.cos(O[0]) * np.sin(O[1])
# y1 = r * np.sin(O[0]) * np.sin(O[1])
# z1 = r * np.cos(O[1])

# x2 = x1 + s * np.cos(O[0]) * np.sin(O[2])
# y2 = y1 + s * np.sin(O[0]) * np.sin(O[2])
# z2 = z1 + s * np.cos(O[2])

# arm, = ax.plot([0, x1], [0, y1], [0, z1], "ro-", label="arm")
# forearm, = ax.plot([x1, x2], [y1, y2], [z1, z2], "bo-", label="forearm")

# set_equal_aspect_3d(ax)

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# # Create sliders
# axcolor = 'lightgoldenrodyellow'
# ax_slider1 = plt.axes([0.1, 0.2, 0.8, 0.03], facecolor=axcolor)
# ax_slider2 = plt.axes([0.1, 0.15, 0.8, 0.03], facecolor=axcolor)
# ax_slider3 = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor)

# slider1 = Slider(ax_slider1, 'Angle 1', 0.0, 360.0, valinit=np.rad2deg(O[0]))
# slider2 = Slider(ax_slider2, 'Angle 2', 0.0, 180.0, valinit=np.rad2deg(O[1]))
# slider3 = Slider(ax_slider3, 'Angle 3', 0.0, 180.0, valinit=np.rad2deg(O[2]))

# # Attach the update function to the sliders
# slider1.on_changed(update)
# slider2.on_changed(update)
# slider3.on_changed(update)

# plt.show()

##################################################
#              Inverse kinematic
##################################################

O = np.array([np.deg2rad(0.0), np.deg2rad(0.0), np.deg2rad(0.0)])
goal = np.array([10, 10, 20])
print(f"total length: {np.linalg.norm(goal)}")




ik = IKHandler(O)
ik.IK(goal)
ik.showPlot(goal)
