# -*- coding: utf-8 -*-
#------------------------------------------
# @file     : mm_script_loopCheck.py
# @brief    : 
# @auther   : 諸星 岬
# @note     : 
#------------------------------------------
from imp import reload
import maya.cmds as cmds
import maya.mel as mel

import os
import glob

import Test03
reload(Test03)

class LoopCheckClass(object):
    def __init__(self):
        pass

    def main(self, type, folders):
        for folder in folders:
            #ログ用フォルダ
            log_folder = os.path.join(folder,"log")
            check_dir(log_folder)
            #スクリプト実行後シーン用フォルダ
            scene_folder = os.path.join(folder,"CheckScene")
            check_dir(scene_folder)

            files = get_open_files(type, folder)
            for file in files:
                self.execute_function_check(file, type, log_folder, scene_folder)

        cmds.headsUpMessage(u'---処理終了---')

    def execute_function_check(self, filePath, type, logDir, SceneDir):
        #ログ記録開始
        logFile_path = os.path.join(logDir,os.path.splitext(os.path.basename(filePath))[0]+"_log.txt")
        cmds.scriptEditorInfo(input="")
        cmds.scriptEditorInfo(historyFilename=logFile_path, writeHistory=True, chf=True )

        if type == "mb":
            #maya シーンファイルのオープン
            print('## Scene File Open >>>>>>>> ' + filePath)
            cmds.file(filePath, f=1, o=1)
        elif type == "fbx":
            mel.eval('FBXProperty "Import|IncludeGrp|Geometry|OverrideNormalsLock" -v 1')
            mel.eval('FBXImportMode -v "add"')
            cmds.file(filePath, i=True, type="FBX")
        else:
            #指定したtypeは不適切
            pass

        # なにか適当に自動処理を書いてください。
        check_function()

        #シーン保存
        rename = os.path.splitext(os.path.basename(filePath))[0]+"_Checked.mb"
        new_file_path = os.path.join(SceneDir,rename)
        #check_dir(new_file_path)

        cmds.file( rename=new_file_path )
        cmds.file(s=1, f=True, typ="mayaBinary")
        print ('## Scene File Save >>>>>>>> ' + rename)

        #ログ記録終了
        cmds.scriptEditorInfo(writeHistory=False)

        #新規シーンを開く
        cmds.file( new=True)

def check_function():
    Test03.main()

#ディレクトリがなければ作成
def check_dir(path):
    if os.path.isdir(path) == False:
        os.makedirs(path)

#指定フォルダから指定タイプのファイルを取得
def get_open_files(type, folderDir):
    files = []
    try:
        find_file = os.path.join(folderDir, "*."+type)
        files = glob.glob(find_file)
    except:
        pass
    return files
