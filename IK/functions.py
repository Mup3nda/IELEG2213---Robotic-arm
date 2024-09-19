import numpy as np
from const import * 

def jacobianIK(O, targetPos): 
    endEffectorPos = ForwardKin(O)
    while(np.linalg.norm(endEffectorPos - targetPos) > 0.5): 
        dO = getDeltaOrientation(O, targetPos)
        O += dO * 0.01 / np.linalg.norm(dO)
        print(f"new O: {O}")
        endEffectorPos = ForwardKin(O)

def getDeltaOrientation(O, targetPos): 
    Jt = np.linalg.pinv(getJacobianTranspose(O))
    endEffectorPos = ForwardKin(O)
    V = targetPos - endEffectorPos
    dO = Jt @ V 
    return dO

def getJacobianTranspose(O):
    # Get the positions
    startPos = np.array([0, 0, 0])  # Base is at the origin
    endPos = ForwardKin(O)  # End effector position
    
    # Define the rotation axes
    zRotation = np.array([0, 0, 1])  # Rotation around the z-axis for DOF 1 (z-rotation)
    
    # Polar rotation axes for arm and forearm (in xy-plane)
    # The polar rotation is around the axes that depend on the current orientation of the joint
    polarArmAxis = np.array([-np.sin(O[0]), np.cos(O[0]), 0])  # Rotation axis perpendicular to radial vector
    polarForearmAxis = polarArmAxis  # Forearm shares the same axis for polar rotation
    
    # Cross products for each joint
    J_A = np.cross(zRotation, endPos - startPos)  # Z-rotation effect
    J_B = np.cross(polarArmAxis, endPos - startPos)  # Polar rotation of arm
    J_C = np.cross(polarForearmAxis, endPos - armKin(O))  # Polar rotation of forearm
    
    # Stack the results into a matrix
    J = np.vstack((J_A, J_B, J_C))
    return J.T

def armKin(O):
    x1 = ARM_LENGHT*np.cos(O[0])*np.sin(O[1])
    y1 = ARM_LENGHT*np.sin(O[0])*np.sin(O[1])
    z1 = ARM_LENGHT*np.cos(O[1])
    return np.array([x1, y1, z1])

def ForwardKin(O): 
    x1 = ARM_LENGHT*np.cos(O[0])*np.sin(O[1])
    y1 = ARM_LENGHT*np.sin(O[0])*np.sin(O[1])
    z1 = ARM_LENGHT*np.cos(O[1])

    x2 = x1+FOREARM_LENGHT*np.cos(O[0])*np.sin(O[2])
    y2 = y1+FOREARM_LENGHT*np.sin(O[0])*np.sin(O[2])
    z2 = z1+FOREARM_LENGHT*np.cos(O[2])
    return np.array([x2, y2, z2])

