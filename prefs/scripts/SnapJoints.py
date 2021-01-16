"""
import SnapJoints 
reload(SnapJoints)
from SnapJoints import * 
snap_joints()
"""

import maya.cmds as cmds


def snap_joints():
    Joints = 'Root', 'Hips', 'Thigh_L', 'Knee_L', 'Ankle_L', 'Toe_L', 'Thigh_R', 'Knee_R', 'Ankle_R', 'Toe_R', \
             'Spine', 'Chest', 'Neck', 'Head', 'Clavicle_L', 'UpperArm_L', 'ForeArm_L', 'Wrist_L', 'Hand_L', \
             'Clavicle_R', 'UpperArm_R', 'ForeArm_R', 'Wrist_R', 'Hand_R', 'FingerA0_L', 'FingerA1_L', 'FingerB0_L', \
             'FingerB1_L', 'Thumb0_L', 'Thumb1_L', 'FingerA0_R', 'FingerA1_R', 'FingerB0_R', 'FingerB1_R', 'Thumb0_R', \
             'Thumb1_R '
    SnapPoints = 'BS_Root', 'BS_Hips', 'BS_LHip', 'BS_LKnee', 'BS_LAnkle', 'BS_LFoot', 'BS_RHip', 'BS_RKnee', \
                 'BS_RAnkle', 'BS_RFoot', 'BS_Spine', 'BS_Chest', 'BS_Neck', 'BS_Head', 'BS_Clavicle_L', \
                 'BS_LUpperArm', 'BS_LLowerArm', 'BS_LWrist', 'BS_LHand', 'BS_Clavicle_R', 'BS_RUpperArm', \
                 'BS_RLowerArm', 'BS_RWrist', 'BS_RHand', 'BS_LFingerA0', 'BS_LFingerA1', 'BS_LFingerB0', \
                 'BS_LFingerB1', 'BS_LThumb0', 'BS_LThumb1', 'BS_RFingerA0', 'BS_RFingerA1', 'BS_RFingerB0', \
                 'BS_RFingerB1', 'BS_RThumb0', 'BS_RThumb1'

    Count = len(Joints)

    for i in range(Count):
        if len(cmds.ls(Joints[i])) > 0 and len(cmds.ls(SnapPoints[i])) > 0:
            cmds.parentConstraint(SnapPoints[i], Joints[i], maintainOffset=False)


def clear_constraints():
    cmds.select('ExportJoints', hi=True)
    constraints = cmds.ls(selection=True, type="constraint")
    cmds.delete(constraints)
