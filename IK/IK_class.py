import numpy as np
from const import * 
import matplotlib.pyplot as plt 
import websockets
import json
import asyncio

class IKHandler: 
    def __init__(self, O):
        self.O = O
        self.x = None
        self.y = None
        self.z = None
    
    async def getCVdata(self, uri = "ws://192.168.0.135:9000"):
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server for receiving coordinates.")
            while True:
                # Receive data from the WebSocket server
                data = await websocket.recv()
                
                # Parse incoming data into x, y, z coordinates
                try:
                    x_str, y_str, z_str = data.split(',')
                    self.x = int(x_str)
                    self.y = int(y_str)
                    self.z = int(z_str)
                    print(f"Received coordinates: x={self.x}, y={self.y}, z={self.z}")

                    goal_pos = np.array([self.x, self.y, self.z])
                    self.IK(goal_pos)
                    self.showPlot(goal_pos)
                
                except ValueError:
                    print(f"Received invalid data: {data}")

                # Optional: Add a short delay if needed
                await asyncio.sleep(0.1)

    def FK(self, section=1):
        x, y, z = 0, 0, 0
        for lim in range(section + 1):
            if lim == 0: 
                x += ARM_LENGHT * np.cos(self.O[0]) * np.sin(self.O[1])
                y += ARM_LENGHT * np.sin(self.O[0]) * np.sin(self.O[1])
                z += ARM_LENGHT * np.cos(self.O[1])
            elif lim == 1:   
                x += FOREARM_LENGHT * np.cos(self.O[0]) * np.sin(self.O[2] + self.O[1]) # kinda løsning?
                y += FOREARM_LENGHT * np.sin(self.O[0]) * np.sin(self.O[2] + self.O[1])
                z += FOREARM_LENGHT * np.cos(self.O[2] + self.O[1])

        return np.array([x, y, z + BASE_HEIGHT])


    def IK(self, targetPos):
        """
        Calculates the new orientation using Jacobian inverse kinematics
        Arguments:
        - O = Orientation in radians
        - targetPos = The goal coordinates
        """
        endEffectorPos = self.FK()
        max_iterations = 5000  # Limit the number of iterations
        iteration = 0
        max_step = np.deg2rad(5)  # Limit max step size to 5 degrees
        epsilon = 1e-6  # Small buffer to avoid exact 0 or pi
        
        while np.linalg.norm(endEffectorPos - targetPos) > 0.5 and iteration < max_iterations:
            dO = self.getDeltaOrientation(targetPos)
            
            norm_dO = np.linalg.norm(dO)
            if norm_dO > 1e-6:  # Avoid division by small numbers
                step = dO * 0.01 / norm_dO
            else:
                step = dO * 0.01
            
            step = np.clip(step, -max_step, max_step)  # Limit the step size
            
            # Update the orientation with the step
            self.O += step
            
            # Conditionally reduce step size if near boundary
            for i, angle in enumerate(self.O):
                if angle < 0.05 or angle > np.pi - 0.05:
                    step[i] *= 0.5
            
            # Ensure that each angle in O is within [epsilon, pi-epsilon]
            self.O = np.clip(self.O, epsilon, np.pi - epsilon)

            endEffectorPos = self.FK()  # Recalculate the end-effector position
            
            if endEffectorPos[2] < 0 or endEffectorPos[1] < 0:
                print("Ground constraint violated, adjusting...")
                self.O -= step * 0.5
                continue

            iteration += 1
    
        if iteration >= max_iterations:
            print("Max iterations reached, solution may not have converged.")
        print(f"The result angle is {np.rad2deg(self.O[0])}, {np.rad2deg(self.O[1])}, {np.rad2deg(self.O[2])}")

    def getDeltaOrientation(self, targetPos): 
        Jt = self.getJacobianTranspose()
        # if you don't transpose the getJacobiantanspose 
        # If i transpose then inverse it then i get ok answer...
        endEffectorPos = self.FK()
        V = targetPos - endEffectorPos
        dO = Jt @ V 
        return dO
    
# TODO finding the correct answer? 
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
        print(f"J_A: {J_A} og J: {J}")
        return J # if you don't transpose then check comment

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
        ax.plot([0, 0], [0, 0], [0, 10], "ro-")
        ax.plot([0, startPos[0]], [0, startPos[1]], [10, startPos[2]], "go-")
        ax.plot([startPos[0], endPos[0]], [startPos[1], endPos[1]], [startPos[2], endPos[2]], "bo-")

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        self.setAspectRatio(ax)
        asyncio.run(self.send("ws://192.168.0.178:9000", targetPos))
        plt.show()

   
    
    async def send(self, ws, targetPos): 
        convertedO = self.O.copy()  

        convertedO[1] = np.pi - convertedO[1]
        convertedO_deg = np.rad2deg(convertedO) 
        convertedO_deg = np.clip(convertedO_deg, 0, 180).astype(int)

        async with websockets.connect(ws) as websocket:
            data = json.dumps(convertedO_deg.tolist()) 
            await websocket.send(data)
            message = await websocket.recv()
            print(f"Sent Orientation: {message}")
            await websocket.close()
