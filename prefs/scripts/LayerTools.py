import maya.cmds as cmds
import Snippets as snip
import maya.mel as mel
import LayerUpdater as layerUpdater


def GetTextName(layer):
    layerTok = layer.split('_')
    layerTok.pop()
    layerName = ''
    for s in layerTok:
        layerName += s
        layerName += '_'
    return layerName[:len(layerName) - 1]


def GetFrameRange(sel):
    if sel is None:
        return ''
    splitName = sel.split('_')
    endFrame = splitName[-1]
    endFrame = endFrame.replace("f", "")
    return endFrame


def SelectLayerObjects():
    mel.eval('string $layers[]={"' + GetSelectedLayers()[0] + '"};layerEditorSelectObjectAnimLayer($layers);')


def GetParentLayer(layer):
    return cmds.animLayer(layer, q=True, parent=True)


def GetAncestors(item, layers):
    done = False
    while not done:
        done = True
        item = GetParentLayer(item)
        if item != 'BaseAnimation':
            layers.append(item)
            done = False
    return layers


def GetChildren(item, layers):
    children = cmds.animLayer(item, q=True, children=True)
    if children is not None:
        for c in children:
            layers.append(c)
    return layers


def DuplicateUnderSelected():
    sel = GetSelectedLayers()
    for s in range(0, len(sel) - 1):
        cmds.animLayer(cmds.animLayer(copy=sel[-1]), edit=True, parent=sel[s])


def SelectLayerNode(layer):
    cmds.select(layer, replace=True, noExpand=True)
    print cmds.ls(selection=True)


def GetSelectedLayerNode(layer):
    cmds.select(layer, replace=True, noExpand=True)
    sel = cmds.ls(selection=True)
    return sel[0]


def GetSelectedLayers():
    layers = []
    for item in cmds.ls(type='animLayer'):
        if cmds.animLayer(item, q=True, selected=True):
            layers.append(item)
    return layers


def FindReplaceInName(find, replaceWith):
    for layer in GetSelectedLayers():
        cmds.rename(layer, layer.replace(find, replaceWith))


def TryFindReplace():
    FindReplaceInName(cmds.textField('FindField', query=True, text=True),
                      cmds.textField('ReplaceField', query=True, text=True))


def TryAddFPSAttr():
    for layer in GetSelectedLayers():
        AddFPSAttribute(layer)


def SortLayersAlphabetically():
    layers = GetSelectedLayers()
    layers.sort()
    for layer_index in range(1, len(layers)):
        cmds.animLayer(layers[layer_index], edit=True, moveLayerAfter=layers[l - 1])


def PlayLayers():
    for layer in GetSelectedLayers():
        layerUpdater.UpdateAnimLayer(layer)
        cmds.currentTime(0)
        if GetFrameRange(layer).isdigit():
            cmds.play(forward=True, wait=True)


def PlayblastLayer(layer):
    path = snip.GetFilePath() + "/PlayBlast/"
    snip.VerifyDirectory(path)
    fileName = path + GetTextName(layer)
    playblastSettings = 'playblast  -format avi -filename "' + fileName + '.avi" -forceOverwrite -sequenceTime 0 ' \
                                                                          '-clearCache 1 -viewer 0 -showOrnaments 1 ' \
                                                                          '-fp 4 -percent 50 -compression "MS-CRAM" ' \
                                                                          '-quality 100; '
    mel.eval(playblastSettings)


def PlayblastSelected():
    for layer in GetSelectedLayers():
        layerUpdater.UpdateAnimLayer(layer)
        if GetFrameRange(layer).isdigit():
            PlayblastLayer(layer)


def LayerRenameWindow():
    renameWindow = cmds.window(title="LayerRename", iconName='LayerRename', resizeToFitChildren=True, te=300, le=1400,
                               widthHeight=(50, 50))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label='Find')
    cmds.textField('FindField', width=50)
    cmds.text(label='Replace')
    cmds.textField('ReplaceField', width=50, enterCommand='TryFindReplace()', alwaysInvokeEnterCommandOnReturn=True)
    cmds.button(label='Replace', command='TryFindReplace()')
    cmds.text(label='Prefix')
    cmds.textField('Prefix', width=50)
    cmds.text(label='Suffix')
    cmds.textField('Suffix', width=50, enterCommand='TryNameAfterParent()', alwaysInvokeEnterCommandOnReturn=True)
    cmds.button(label='Rename', command='TryNameAfterParent()')
    cmds.button(label='CopyUnder', command='DuplicateUnderSelected()')
    cmds.button(label='Add Fps Attribute', command='TryAddFPSAttr()')
    cmds.setParent('..')
    cmds.showWindow(renameWindow)


def GetSelectedOrAllLayers():
    selected = GetSelectedLayers()
    if len(selected) == 0:
        selected = cmds.ls(type='animLayer')
    return selected


def TryNameAfterParent():
    for layer in GetSelectedLayers():
        par = cmds.animLayer(layer, query=True, parent=True)
        if par != 'BaseAnimation':
            cmds.rename(layer, cmds.textField('Prefix', query=True, text=True)
                        + GetTextName(par) + cmds.textField('Suffix', query=True, text=True))


def ExpandLayer(layer):
    if cmds.animLayer(layer, query=True, children=True):
        mel.eval('animLayerExpandCollapseCallback "' + layer + '" 1;')


def CollapseLayer(layer):
    if cmds.animLayer(layer, query=True, children=True):
        mel.eval('animLayerExpandCollapseCallback "' + layer + '" 0;')


def ExpandSelectedLayers():
    for layer in GetSelectedOrAllLayers():
        ExpandLayer(layer)


def CollapseSelectedLayers():
    for layer in GetSelectedOrAllLayers():
        CollapseLayer(layer)


def AddFPSAttribute(layer):
    SelectLayerNode(layer)
    cmds.addAttr(longName="fps", attributeType="enum", enumName="30 fps:60 fps:", keyable=True)


def GetFPSAttribute(layer):
    if cmds.attributeQuery('fps', node=layer, exists=True):
        return cmds.getAttr(layer + ".fps", asString=True)
    else:
        return "30 fps"
