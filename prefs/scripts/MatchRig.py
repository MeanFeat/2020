"""
import MatchRig 
reload(MatchRig)
from MatchRig import * 
DoMatch()
"""

import maya.cmds as cmds


def SnapAll(mov, tar):
    pos = (cmds.xform(tar, q=True, ws=True, rp=True))
    cmds.move(pos[0], pos[1], pos[2], mov, ws=True)
    rotX = cmds.getAttr(tar + '.rotateX')
    rotY = cmds.getAttr(tar + '.rotateY')
    rotZ = cmds.getAttr(tar + '.rotateZ')
    cmds.setAttr(mov + '.rotateX', rotX)
    cmds.setAttr(mov + '.rotateY', rotY)
    cmds.setAttr(mov + '.rotateZ', rotZ)


def SnapPar(movesel, refsel):
    pc = cmds.parentConstraint(refsel, movesel, mo=False, w=1000.0)
    cmds.delete(pc)


def SnapPos(movesel, refsel):
    pc = cmds.pointConstraint(refsel, movesel, mo=False, w=1000.0)
    cmds.delete(pc)


def SnapParPair(item, dest, all=False):
    for side in {"_L", "_R"}:
        if all:
            SnapAll(item + side, dest + side)
        else:
            SnapPar(item + side, dest + side)


def SnapPolePair(item):
    for side in {"_L", "_R"}:
        SetPoleVector(item + side)


def ToggleIK(attr):
    for side in {"_L", "_R"}:
        cmds.setAttr("LegikHandle1" + side + ".ikBlend", attr)
        cmds.setAttr("LegikHandle2" + side + ".ikBlend", attr)
        cmds.setAttr("ikHandleArm" + side + ".ikBlend", attr)


def SetPoleVector(pV):
    cmds.makeIdentity(pV, apply=True, t=1)
    cmds.move(-100.0, pV, objectSpace=True, moveZ=True)
    cmds.setAttr(pV + '.rotateX', 0)
    cmds.setAttr(pV + '.rotateY', 0)
    cmds.setAttr(pV + '.rotateZ', 0)
    cmds.makeIdentity(pV, apply=True, t=1)


# Spine and Head
def Center():
    SnapPar('GrpCOGCtrl', 'AR_CoG')
    SnapPar('GrpSpineCtrl', 'AR_SpinePointer')
    SnapPar('ChestHelper', 'AR_Chest')
    SnapPar('GrpNeckCtrl', 'AR_Neck')
    SnapPar('GrpHeadCtrl', 'AR_Head')
    SnapPar('GrpLookAtCtrl', 'AR_Head')
    SnapPar('AimNull', 'AR_Head')
    SnapAll('HeadAimBlendHelper', 'AR_Head')


def Legs():
    # Legs
    SnapPar('HipHelper_L', 'AR_LegHelper_L')
    cmds.parentConstraint('HipsCtrl', 'HipHelper_L', mo=True)
    SnapPar('IK_Helper0_L', 'AR_LegHelper_L')
    SnapPar('IKLeg0_L', 'AR_Thigh_L')
    SnapPar('IKLeg1_L', 'AR_Shin_L')
    SnapPar('AnkleHelper_L', 'AR_Foot_L')
    SnapPar('GrpFootCtrl_L', 'AR_Foot_L')
    SnapPar('GrpFootBall_L', 'AR_Toe_L')
    SnapAll('IKLeg2_L', 'AR_Foot_L')
    SnapAll('IKLeg3_L', 'AR_Toe_L')
    SnapPar('LegikHandle1_L', 'AR_Foot_L')
    SnapAll('LegikHandle2_L', 'AR_Foot_L')
    # cmds.parentConstraint( 'HeelCtrl_L', 'LegikHandle1_L', mo=True)
    SnapPar('HipHelper_R', 'AR_LegHelper_R')
    cmds.parentConstraint('HipsCtrl', 'HipHelper_R', mo=True)
    SnapPar('IK_Helper0_R', 'AR_LegHelper_R')
    SnapPar('IKLeg0_R', 'AR_Thigh_R')
    SnapPar('IKLeg1_R', 'AR_Shin_R')
    SnapPar('AnkleHelper_R', 'AR_Foot_R')
    SnapPar('GrpFootCtrl_R', 'AR_Foot_R')
    SnapPar('GrpFootBall_R', 'AR_Toe_R')
    SnapAll('IKLeg2_R', 'AR_Foot_R')
    SnapAll('IKLeg3_R', 'AR_Toe_R')
    SnapPar('LegikHandle1_R', 'AR_Foot_R')
    SnapAll('LegikHandle2_R', 'AR_Foot_R')
    # cmds.parentConstraint( 'HeelCtrl_R', 'LegikHandle1_R', mo=True)


def Arms():
    # Arms
    SnapPar('gClavicleCtrl_L', 'AR_Clavicle_L')
    SnapPar('ShoulderHelper_L', 'AR_UpperArm_L')
    SnapPar('IKArm0_L', 'AR_UpperArm_L')
    SnapPar('LUArmFK', 'AR_UpperArm_L')
    SnapAll('BlendArm0_L', 'AR_UpperArm_L')
    SnapPar('IKArmVector_L', 'AR_ForeArm_L')
    SetPoleVector('IKArmVector_L')
    SnapPar('IKArm1_L', 'AR_ForeArm_L')
    SnapPar('gFarm_L', 'AR_ForeArm_L')
    SnapAll('BlendArm1_L', 'AR_ForeArm_L')
    SnapPar('GrpIKHand_L', 'AR_Hand_L')
    SnapPar('IKArm2_L', 'AR_Hand_L')
    # Right
    SnapPar('gClavicleCtrl_R', 'AR_Clavicle_R')
    SnapPar('ShoulderHelper_R', 'AR_UpperArm_R')
    SnapPar('IKArm0_R', 'AR_UpperArm_R')
    SnapPar('RUArmFK', 'AR_UpperArm_R')
    SnapAll('BlendArm0_R', 'AR_UpperArm_R')
    SnapPar('IKArmVector_R', 'AR_ForeArm_R')
    SetPoleVector('IKArmVector_R')
    SnapPar('IKArm1_R', 'AR_ForeArm_R')
    SnapPar('gFarm_R', 'AR_ForeArm_R')
    SnapAll('BlendArm1_R', 'AR_ForeArm_R')
    SnapPar('GrpIKHand_R', 'AR_Hand_R')
    SnapPar('IKArm2_R', 'AR_Hand_R')


def Hands():
    # hands
    SnapPar('GrpThumb0_L', 'AR_Thumb0_L')
    SnapPar('GrpThumb1_L', 'AR_Thumb1_L')
    SnapPar('GrpFingerA0_L', 'AR_FingerA0_L')
    SnapPar('GrpFingerA1_L', 'AR_FingerA1_L')
    SnapPar('GrpFingerB0_L', 'AR_FingerB0_L')
    SnapPar('GrpFingerB1_L', 'AR_FingerB1_L')
    SnapPar('GrpThumb0_R', 'AR_Thumb0_R')
    SnapPar('GrpThumb1_R', 'AR_Thumb1_R')
    SnapPar('GrpFingerA0_R', 'AR_FingerA0_R')
    SnapPar('GrpFingerA1_R', 'AR_FingerA1_R')
    SnapPar('GrpFingerB0_R', 'AR_FingerB0_R')
    SnapPar('GrpFingerB1_R', 'AR_FingerB1_R')


def AfterIK():
    SnapPar('KneeVector_SideNull_L', 'KneeVector_SideNullHelper_L')
    SnapPar('KneeVector_L', 'KneeVectorHelper_L')
    SnapPar('KneeVector_SideNull_R', 'KneeVector_SideNullHelper_R')
    SnapPar('KneeVector_R', 'KneeVectorHelper_R')

    SnapAll('BlendArm2_L', 'ikHandleArm_L')
    SnapPar('GrpFKHand_L', 'AR_Hand_L')
    SnapPos('BlendWrist_L', 'AR_Wrist_L')
    SnapAll('BlendArm2_R', 'AR_Hand_R')
    SnapPar('GrpFKHand_R', 'AR_Hand_R')
    SnapPos('BlendWrist_R', 'AR_Wrist_R')


def DoMatch():
    ToggleIK(0)
    Center()
    Legs()
    Arms()
    ToggleIK(1)
    AfterIK()
    Hands()
