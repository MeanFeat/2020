import maya.cmds as cmds


def PinTranslate(sel):
    for s in sel:
        pin_name = s + "_TranslatePin"
        if cmds.ls(pin_name):
            cmds.delete(pin_name)
            cmds.delete("*:"+pin_name)
        else:
            temp_null = cmds.spaceLocator(name=pin_name)
            cmds.delete(cmds.pointConstraint(s, temp_null, mo=False))
            cmds.pointConstraint(temp_null, s, mo=True)
            cmds.select(sel)


def PinRotate(sel):
    for s in sel:
        pin_name = s + "_RotatePin"
        if cmds.ls(pin_name):
            cmds.delete(pin_name)
            cmds.delete("*:"+pin_name)
        else:
            temp_null = cmds.spaceLocator(name=pin_name)
            cmds.delete(cmds.parentConstraint(s, temp_null, mo=False))
            cmds.orientConstraint(temp_null, s, mo=True)
            cmds.select(sel)
