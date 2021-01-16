import maya.cmds as cmds
import maya.mel as mel
import PinTools as pin

axis = ['X', 'Y', 'Z']
attrs = ['translate', 'rotate', 'scale']


def bind_reference():
    sel = cmds.ls(selection=True)
    if len(sel) != 2:
        print('Please select only the reference root followed by the target root.')
    else:
        cmds.select(sel[0], replace=True, hierarchy=True)
        ref = cmds.ls(selection=True, type="joint")
        cmds.select(sel[1], replace=True, hierarchy=True)
        joints = cmds.ls(selection=True, type="joint")
        for i in range(0, len(joints)):
            cmds.parentConstraint(ref[i], joints[i], mo=True)


def generalize_files():
    files = cmds.ls(type="file")
    for f in files:
        path = cmds.getAttr(f + ".fileTextureName")
        splitPath = path.split("/")
        found = False
        for s in splitPath:
            if s == "doom3":
                found = True
                path = "%PANIC_BASE_PATH%"
            if found:
                path += "/" + s
        cmds.setAttr(f + ".fileTextureName", path, type="string")
        print(path)


def get_selection(t=""):
    if t == "":
        return cmds.ls(selection=True)
    else:
        return cmds.ls(selection=True, type=t)


def clean_up_materials(meshes):
    for item in cmds.ls(type="lambert"):
        cmds.setAttr(item + ".incandescence", 0.0, 0.0, 0.0)
    for texture in cmds.ls(type="place2dTexture"):
        cmds.setAttr(texture + ".repeatV", 1)
    for m in meshes:
        cmds.polyFlipUV(m, flipType=1, local=1, usePivot=True)
        cmds.select(m + ".f[0:" + str(cmds.polyEvaluate(m, face=True) - 1) + "]", replace=True)
        cmds.polyEditUV(u=0, v=1)
    cmds.select(clear=True)


def flip_ui_uvs():
    cmds.select("*UI*", replace=True)
    for m in cmds.ls(selection=True):
        cmds.polyFlipUV(m, flipType=0, local=1, usePivot=True)
    cmds.select(clear=True)


def clean_up_joints(joints, root, origin):
    pin.PinTranslate(joints)
    pin.PinRotate(joints)
    cmds.select(root)
    cmds.makeIdentity()
    cmds.setKeyframe(joints)
    cmds.delete("*TranslatePin")
    cmds.delete("*RotatePin")
    cmds.refresh(force=True)
    cmds.cutKey(joints)
    for j in joints:
        for ax in axis:
            cmds.setAttr(j + '.scale' + ax, 1.0)
        if "lasersight" in str(j) or "barrel" in str(j) or "wepFlash" in str(j):
            cmds.setAttr(j + ".rotateY", 180);


def mirror_root():
    cmds.select("*origin")
    origin = get_selection("joint")
    root = cmds.listRelatives(origin, parent=True)
    cmds.select(root)
    cmds.setAttr(root[0] + ".scaleY", -1.0)
    return root, origin


def mirror_md5mesh():
    root, origin = mirror_root()
    cmds.CopySelected()
    cmds.select(cmds.ls(type="mesh"), replace=True)
    cmds.delete(constructionHistory=True)
    dup_meshes = cmds.duplicate()
    clean_up_materials(dup_meshes)
    cmds.select(dup_meshes, replace=True)
    cmds.parent(world=True)
    for obj in get_selection():
        cmds.polyNormal(obj, normalMode=0)
        for ax in axis:
            for attr in attrs:
                cmds.setAttr(obj + '.' + attr + ax, lock=0)

    cmds.delete("meshes")

    cmds.select(origin, hi=True)
    joints = get_selection()
    joints.pop(0)

    clean_up_joints(joints, root, origin)

    cmds.select(dup_meshes, replace=True)
    cmds.select(joints, add=True)
    cmds.delete(constructionHistory=True)
    cmds.delete(cmds.ls(type="dagPose"))
    cmds.SmoothBindSkin()

    cmds.PasteSelected()
    cmds.select(get_selection(), hierarchy=True)
    pasted_meshes = get_selection("mesh")

    dup_meshes.sort()
    pasted_meshes.sort()

    for i in range(0, len(dup_meshes)):
        cmds.select(pasted_meshes[i], replace=True)
        cmds.select(dup_meshes[i], add=True)
        cmds.CopySkinWeights(surfaceAssociation="closestPoint", influenceAssociation="oneToOne")

    cmds.delete(cmds.ls("pasted_*"))
    flip_ui_uvs()
    cmds.select(clear=True)
    generalize_files()
