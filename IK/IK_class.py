import numpy as np
from const import * 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

class IKHandler: 
    def __init__(self, O):
        self.O = O


    def FK(self, section=1):
        x, y, z = 0, 0, 0

        for lim in range(section + 1):
            if lim == 0:  # First segment (arm)
                x += ARM_LENGHT * np.cos(self.O[0]) * np.sin(self.O[1])
                y += ARM_LENGHT * np.sin(self.O[0]) * np.sin(self.O[1])
                z += ARM_LENGHT * np.cos(self.O[1])
            else:  # Subsequent segments (forearms)
                x += FOREARM_LENGHT * np.cos(self.O[0]) * np.sin(self.O[lim + 1])
                y += FOREARM_LENGHT * np.sin(self.O[0]) * np.sin(self.O[lim + 1])
                z += FOREARM_LENGHT * np.cos(self.O[lim + 1])
        
        return np.array([x, y, z])

    def IK(self, targetPos): 
        """
        # Task
        Calculates the new orientaion by using jacobian inverse kinematics calculation
        # Arguments 
        - O = Orientation in radians 
        - targetPos = The goal coordinates
        """
        endEffectorPos = self.FK()
        while(np.linalg.norm(endEffectorPos - targetPos) > 0.5): 
            dO = self.getDeltaOrientation(targetPos)
            self.O += dO * 0.01 / np.linalg.norm(dO)
            print(f"new O: {self.O}")
            endEffectorPos = self.FK()

    def getDeltaOrientation(self, targetPos): 
        Jt = np.linalg.pinv(self.getJacobianTranspose())
        endEffectorPos = self.FK()
        V = targetPos - endEffectorPos
        dO = Jt @ V 
        return dO

    def getJacobianTranspose(self):
        startPos = np.array([0, 0, 0])  # Base is at the origin
        endPos = self.FK()  # End effector position

        zRotation = np.array([0, 0, 1])  
        polarArmAxis = np.array([-np.sin(self.O[0]), np.cos(self.O[0]), 0]) 
        polarForearmAxis = polarArmAxis  
        
        J_A = np.cross(zRotation, endPos - startPos)  
        J_B = np.cross(polarArmAxis, endPos - startPos)  
        J_C = np.cross(polarForearmAxis, endPos - self.FK(0))  
        
        J = np.vstack((J_A, J_B, J_C))
        return J.T

    def setAspectRatio(self, ax):
        extents = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
        centers = np.mean(extents, axis=1)
        max_range = np.max(np.ptp(extents, axis=1)) / 2

        ax.set_xlim3d([centers[0] - max_range, centers[0] + max_range])
        ax.set_ylim3d([centers[1] - max_range, centers[1] + max_range])
        ax.set_zlim3d([centers[2] - max_range, centers[2] + max_range])
    
    def showPlot(self, targetPos): 
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        startPos = self.FK(0)
        endPos = self.FK()

        ax.plot(targetPos[0], targetPos[1], targetPos[2], "ro-")
        ax.plot([0, startPos[0]], [0, startPos[1]], [0, startPos[2]], "go-")
        ax.plot([startPos[0], endPos[0]], [startPos[1], endPos[1]], [startPos[2], endPos[2]], "bo-")

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        self.setAspectRatio(ax)
        plt.show()
