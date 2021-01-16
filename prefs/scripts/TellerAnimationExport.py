import maya.mel as mel

import maya.cmds as cmds
import string

keywords = ['Enemies', 'Guardians', 'NPC', 'Player']  # Shared folder names from source and import


def SelectExportJoints():
    cmds.select('*:ExportJoints', replace=True, hi=True)


def GetExportSettings(file_path, file_name):
    mel.eval('FBXExportBakeComplexAnimation -v 1;')
    start = cmds.playbackOptions(q=1, min=1)
    end = cmds.playbackOptions(q=1, max=1)
    mel.eval("FBXExportBakeComplexStart -v " + str(start))
    mel.eval("FBXExportBakeComplexEnd -v " + str(end))
    return 'FBXExport -f "' + file_path + file_name + '.fbx" -s;'


def BuildFileName(splitPath):
    fileNameFull = splitPath[-1]  # Remove path
    fileNameFull = fileNameFull.split('.')[0]  # Remove file extension
    fileNameFull = fileNameFull.split('_')
    fileNameFull[0] = "ANIM"
    result_fileName = ''
    for e in range(len(fileNameFull)):
        result_fileName += fileNameFull[e]
        if e < len(fileNameFull) - 1:
            result_fileName += "_"
    return result_fileName


def GetFilePath():
    splitPath = cmds.file(query=True, expandName=True)  # Get the full path file name
    splitPath = splitPath.split('/')
    result_fileName = BuildFileName(splitPath)  # Replace SK_ with ANIM_
    splitPath.pop()  # Remove file name so only path remains
    result_path = ''
    for item in splitPath:  # Set to Export Path
        if item == 'Content':
            result_path += 'Content/Import/Animations/'
            break
        result_path += item + "/"
    for item in splitPath:  # Add key folder
        for key in keywords:
            if item == key:
                result_path += key + '/'
                break
    return result_path, result_fileName


origSelection = cmds.ls(selection=True)
SelectExportJoints()
path, fileName = GetFilePath()
mel.eval(GetExportSettings(path, fileName))
cmds.select(origSelection)
