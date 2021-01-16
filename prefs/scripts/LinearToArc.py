import maya.cmds as cmds
import LayerTools as lt


def LinearToArc(radius):
    diameter = radius * 2
    origframe = cmds.currentTime(q=True)
    selection = cmds.ls(selection=True)
    if len(selection) == 0:
        cmds.warning("Select the object with the travel distance")
        return
    tZ = "%s.translateZ" % selection[0]
    tX = "%s.translateX" % selection[0]
    startZ = cmds.getAttr(tZ, t=0)
    endZ = cmds.getAttr(tZ, t=30)
    cmds.cutKey(selection[0], clear=True)
    newX = cmds.getAttr(tX)
    newX += (diameter / 2.0)
    if startZ != endZ:
        pivot = cmds.spaceLocator(name="TurnPivot")
        cmds.animLayer(lt.GetSelectedLayers()[0], edit=True, addSelectedObjects=True)
        pivotName = pivot[0]
        distance = endZ - startZ
        pi = 3.142857142857143
        circumf = diameter * pi
        degrees = (distance / circumf) * 360
        cmds.setAttr(tZ, 0)
        cmds.setAttr(tX, newX)
        cmds.parentConstraint(pivot, selection[0], mo=True)
        cmds.setKeyframe(pivot, t=0)
        cmds.currentTime(30)
        # animate the arc
        rY = "%s.rotateZ" % pivotName
        cmds.setAttr(rY, -degrees)
        cmds.setKeyframe(pivot, t=30)
        cmds.currentTime(origframe)
        # set the curve to linear
        rotCurve = "%s_rotateZ" % pivotName
        cmds.selectKey(rotCurve, r=True)
        cmds.keyTangent(itt="linear", ott="linear")
        cmds.setInfinity(poi="cycleRelative")
        cmds.bakeResults(selection[0], t=(0, 30))
    if startZ == endZ:
        cmds.warning("The object is not traveling")


def LinearToArcCmd():
    result = cmds.promptDialog(
        title='Set Diameter of Arc',
        message='Diameter:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

    if result == 'OK':
        inputTxt = cmds.promptDialog(query=True, text=True)
        LinearToArc(float(inputTxt))
