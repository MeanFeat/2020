import maya.cmds as cmds
import LayerTools as layerTools


def CreateScriptJob():
    return cmds.scriptJob(e=("animLayerRefresh", UpdateSelectedAnimLayer), killWithScene=True, compressUndo=True)


def UpdateSelectedAnimLayer():
    for item in cmds.ls(type='animLayer'):
        if cmds.animLayer(item, q=True, selected=True):
            UpdateAnimLayer(item)


def UpdateAnimLayer(layer):
    unmute = []
    for item in cmds.ls(type='animLayer'):
        if item == layer:
            if layerTools.GetFrameRange(item).isdigit():
                UpdateFramesPerSecond(layerTools.GetFPSAttribute(item))
                cmds.playbackOptions(max=layerTools.GetFrameRange(item))
            unmute.append(item)
            unmute = layerTools.GetAncestors(item, unmute)
            unmute = layerTools.GetChildren(item, unmute)
        elif item != 'BaseAnimation':
            cmds.setAttr(item + ".lock", 1)
            cmds.setAttr(item + ".mute", 1)
    for u in unmute:
        cmds.setAttr(u + ".mute", 0)
        cmds.setAttr(u + ".lock", 0)


def UpdateFramesPerSecond(string):
    cmds.currentUnit(time='ntsc')
    if string == "60 fps":
        cmds.currentUnit(time='ntscf')
