import maya.cmds as cmds
import maya.mel as mel
import LayerTools as layerTools
import LayerUpdater as layerUpdater
import Snippets as snip
import collections
import winsound

ProgressTuple = collections.namedtuple('ProgressWindow', ['window', 'control'])


def SelectExportJoints():
    cmds.select('Rig:root', hi=True)
    exportJoints = cmds.ls(selection=True, type='joint')
    cmds.select(exportJoints)


def GetExportSettings(exportLayer, start=None, end=None, fileName=''):
    mel.eval('FBXExportBakeComplexAnimation -v 1;')
    minimum = str(0) if start is None else str(start)
    maximum = 1
    layerFrameRange = layerTools.GetFrameRange(exportLayer)
    if layerFrameRange.isdigit():
        maximum = layerFrameRange
    if end is not None:
        maximum = str(end)
    mel.eval("FBXExportBakeComplexStart -v " + minimum)
    mel.eval("FBXExportBakeComplexEnd -v " + maximum)
    if fileName is None or len(fileName) == 0:
        fileName = layerTools.GetTextName(exportLayer)
    path = snip.GetFilePath() + "/FBX/"
    snip.VerifyDirectory(path)
    return 'FBXExport -f "' + path + fileName + '.fbx" -s;'


def IsExportable(item):
    return layerTools.GetFrameRange(item).isdigit()


def ExportLayer(settings):
    origSelection = cmds.ls(selection=True)
    SelectExportJoints()
    mel.eval(settings)
    cmds.select(origSelection)


def ExportSelectedLayers():
    selected = layerTools.GetSelectedLayers()
    if cmds.animLayer(layerTools.GetParentLayer(selected[0]), query=True, baseAnimCurves=True) is not None:
        result = cmds.confirmDialog(title='Warning:', message="BaseAnim layer not empty", button=['Continue', 'Cancel'])
        if result == 'Cancel':
            snip.FailExit('Export canceled because base anim layer is not empty')
    prog = CreateProgressWindow(len(selected))
    for item in selected:
        cmds.progressBar(prog.control, edit=True, step=1)
        if IsExportable(item):
            progressStatus = layerTools.GetTextName(item) + '...'
            cmds.window(prog.window, edit=True, title=progressStatus)
            layerUpdater.UpdateAnimLayer(item)
            ExportLayer(GetExportSettings(item))
    cmds.deleteUI(prog.window)
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)


def ExportLayerRange(start, end, name):
    cmds.playbackOptions(min=start, max=end)
    ExportLayer(GetExportSettings(None, start, end, name))
    layerUpdater.UpdateSelectedAnimLayer()


def ExportAll():
    for item in cmds.ls(type='animLayer'):
        if item != 'BaseAnimation':
            if IsExportable(item):
                layerUpdater.UpdateAnimLayer(item)
                ExportLayer(GetExportSettings(item))


def TryExportRange():
    start = cmds.intFieldGrp('rangeFields', query=True, value1=True)
    end = cmds.intFieldGrp('rangeFields', query=True, value2=True)
    name = cmds.textField('nameField', query=True, text=True)
    if start > end:
        snip.FailExit("Range start must be larger than end")
    if len(name) == 0:
        snip.FailExit("Name not valid")
    ExportLayerRange(start, end, name)


def ExportRangeWindow():
    exportRangeWin = cmds.window(title="Export Layer Range", iconName='Export Layer Range', resizeToFitChildren=True,
                                 te=300, le=1400, widthHeight=(50, 50))
    cmds.columnLayout(adjustableColumn=True)
    cmds.intFieldGrp('rangeFields', numberOfFields=2, label='Range', value1=0, value2=20, columnAlign2=('Left', 'Left'))
    cmds.textField('nameField', width=50)
    cmds.button(label='Export', command='TryExportRange()')
    cmds.setParent('..')
    cmds.showWindow(exportRangeWin)


def CreateProgressWindow(size):
    win = cmds.window(title='Exporting Layers', toolbox=True)
    cmds.columnLayout()
    progWin = ProgressTuple(win, cmds.progressBar(maxValue=size, width=400))
    cmds.showWindow(progWin.window)
    return progWin
