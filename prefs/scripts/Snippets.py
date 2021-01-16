import maya.cmds as cmds
import maya.mel as mel
import os
import sys


def GetFilePath():
    splitPath = cmds.file(query=True, expandName=True)
    splitPath = splitPath.split('/')
    splitPath.pop()
    path = "";
    for item in splitPath:
        path += item + "/"
    return path


def FailExit(message):
    cmds.error(message)
    sys.exit()


def GetFileName():
    fileName = cmds.file(query=True, expandName=True)
    fileName = fileName.split('.')
    fileName = fileName[0].split('/')
    return fileName[-1]


def GetFileExtension():
    fileName = cmds.file(query=True, expandName=True)
    fileName = fileName.split('.')
    return '.' + fileName[-1]


def CreateNullOnObject(item, suffix):
    tempNull = cmds.group(empty=True, name=item + suffix)
    tempPC = cmds.parentConstraint(item, tempNull, mo=False)
    cmds.delete(tempPC)
    cmds.makeIdentity(tempNull, apply=True, t=1, r=0, s=0)
    return tempNull


def VerifyDirectory(fullPath):
    if not os.path.isdir(fullPath):
        os.makedirs(fullPath)
