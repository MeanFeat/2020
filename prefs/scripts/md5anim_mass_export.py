import os
import sys
import stat
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pmc
import Snippets as snip

mir_directory = snip.GetFilePath() + 'mirror/'
export_base_directory = 'D:/Gamedev/Archiact/WFH_PANIC/doom3/base/models/md5/weapons/'


def get_file_data():
    if not cmds.ls('MD5MassExport'):
        cmds.confirmDialog(title='Error', message='MD5MassExport not found!', button=['OK'])
        sys.exit()
    ref = cmds.getAttr('MD5MassExport.commands[0]')
    exp_dir = export_base_directory + cmds.getAttr('MD5MassExport.commands[1]')
    ignore = cmds.getAttr('MD5MassExport.commands[2]')
    return ref, exp_dir, ignore


def get_mirror_filenames(directory):
    result = []
    for subdir, dirs, files in os.walk(directory):
        for f in files:
            result.append(f)
    return result


def get_export_filenames(directory):
    result = []
    for subdir, dirs, files in os.walk(directory):
        for f in files:
            if '_left.md5anim' in f:
                result.append(f)
    return result


def load_reference(f):
    split = f.split('.')
    ext = 'mayaAscii' if str(split[-1]) == "ma" else 'mayaBinary'
    cmd = 'file -loadReference "' + reference_name + '" -type "' + ext + '" -options "v=0;" "' \
          + mir_directory + f + '";'
    mel.eval(cmd)


def export(cmd):
    max_time = 9999999
    cmds.playbackOptions(animationEndTime=max_time)
    cmds.select("*:ref*")
    keyframes = pmc.keyframe(q=True, time=(0, max_time))
    end = keyframes[-1] + 1
    cmds.playbackOptions(animationEndTime=end, maxTime=end)
    mel.eval(cmd)
    cmds.select(clear=True)


def mass_export(mir, exp, exp_dir):
    for i in range(0, len(mir)):
        load_reference(mir[i])
        cmd = 'file -force -options "" -type "MD5Anim" -pr -ea "' + exp_dir + '/' + exp[i] + '";'
        export(cmd)


def build_print_list(file_list):
    result = ""
    for i in range(0, len(file_list)):
        result += "'" + file_list[i] + "'"
        if i < len(file_list) - 1:
            result += ", "
    return result


def set_files_writable(directory, file_list):
    for f in file_list:
        full_path_name = directory + '/' + f
        os.chmod(full_path_name, stat.S_IWRITE)


def md5anim_mass_export_main():
    mir_files = get_mirror_filenames(mir_directory)
    export_files = get_export_filenames(export_directory)
    set_files_writable(export_directory, export_files)

    for mf in mir_files:
        split_filename = mf.split('.')
        if str(split_filename[-1]) != "mb" and str(split_filename[-1]) != "ma":
            print("Removing none maya file: " + mf)
            mir_files.remove(mf)

    if ignore_keyword != "":
        for mf in mir_files:
            if mf.find(ignore_keyword) != -1:
                print("Removing: " + mf)
                mir_files.remove(mf)

    if len(mir_files) is len(export_files):
        mass_export(mir_files, export_files, export_directory)
    else:
        cmds.confirmDialog(title='Error', message='Mismatched file count. See log for instructions.', button=['OK'])
        print("== Sort and run this command. ==")
        print("mir = [" + build_print_list(mir_files) + "]")
        print("exp = [" + build_print_list(export_files) + "]")
        print("mass_export(mir, exp, \"" + export_directory + "\")")
        sys.exit()


reference_name, export_directory, ignore_keyword = get_file_data()
md5anim_mass_export_main()
