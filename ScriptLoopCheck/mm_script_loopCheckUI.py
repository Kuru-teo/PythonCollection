# -*- coding: utf-8 -*-
#------------------------------------------
# @file     : mm_script_loopCheckUI.py
# @brief    : 
# @auther   : 諸星 岬
# @note     : 
#------------------------------------------
from maya import OpenMayaUI

import os
import imp
try:
    imp.find_module('PySide2')
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    Package = 'PySide2'

except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *
    Package = 'PySide'

try:
    import shiboken
except:
    import shiboken2 as shiboken

from . import mm_script_loopCheck
imp.reload(mm_script_loopCheck)


#--------------------------グローバル変数-------------------------------------
ptr = OpenMayaUI.MQtUtil.mainWindow()
parent = shiboken.wrapInstance(int(ptr), QWidget)

WindowObjName = "mm_script_loopCheck"
folderPath = os.path.dirname(__file__)
iniFileName = "mm_script_loopCheck_UIsetting"

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.file_path_list = None
        self.file_type = "mb"
        self.loop_checker = mm_script_loopCheck.LoopCheckClass()
        #UI形状
        self.settingUI()
        #UI読み込み
        self.buildUI()
        #INIファイルの設定・読み込み
        self.iniFileSetting(folderPath,iniFileName)
        self.loadSettings()
    
    def buildUI(self):
        #Window基本情報
        self.setObjectName(WindowObjName)
        self.setGeometry(400, 800, 650, 600)
        self.resize(250,300)
        self.setWindowTitle(WindowObjName)
        #Windowにwidgetを追加
        self.setCentralWidget(self.mainWidget)
    
    def settingUI(self):
        #---------------------------子layoutにWidgetの追加---------------------------
        #----------1段目
        hboxA = QHBoxLayout()
        layA = QVBoxLayout()

        model = QStandardItemModel()
        self.listView = ListView()
        self.listView.setObjectName("mm_lc_listView")
        self.listView.setModel(model)
        layA.addWidget(self.listView)

        #self.qlineA = QLineEdit(self)
        self.groupboxA = QGroupBox("file folder path list")
        self.groupboxA.setLayout(layA)
        hboxA.addWidget(self.groupboxA)
        self.buttonA = QPushButton(u"Reset List")
        self.buttonA.setObjectName("mm_lc_clear_list")
        self.buttonA.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.buttonA.clicked.connect(self.listView.clearList)
        layA.addWidget(self.buttonA)

        #----------2段目
        hboxC = QHBoxLayout()
        layC = QHBoxLayout()
        
        self.fileTypeGroup = QButtonGroup(self)
        self.radioBtn1 = QRadioButton("mb")
        self.radioBtn1.setObjectName("mm_fileTypeGroup_mb")
        self.radioBtn1.clicked.connect(lambda x=0, y=self.radioBtn1: self.CallbackRadioButton(button=y))
        self.fileTypeGroup.addButton(self.radioBtn1)
        self.radioBtn2 = QRadioButton("fbx")
        self.radioBtn2.setObjectName("mm_fileTypeGroup_fbx")
        self.radioBtn2.clicked.connect(lambda x=0, y=self.radioBtn2: self.CallbackRadioButton(button=y))
        self.fileTypeGroup.addButton(self.radioBtn2)
        self.radioBtn1.setChecked(True)

        layC.addWidget(self.radioBtn1)
        layC.addWidget(self.radioBtn2)

        self.groupboxE = QGroupBox("file type")
        self.groupboxE.setLayout(layC)

        hboxC.addWidget(self.groupboxE)
        
        #----------3段目
        hboxD = QHBoxLayout()
        layE = QVBoxLayout()
        self.spaceA = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.buttonC = QPushButton(u"\nStart Loop Check\n")
        self.buttonC.setObjectName("mm_lc_execute")
        self.buttonC.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.buttonC.clicked.connect(self.execution_button)
        layE.addWidget(self.buttonC)

        self.groupboxB = QGroupBox("execution button")
        self.groupboxB.setLayout(layE)
        hboxD.addWidget(self.groupboxB)
        
        #---------------------------親layoutに子layoutを追加---------------------------
        vParentBox = QVBoxLayout()
        vParentBox.setContentsMargins(20,10,20,10)
        vParentBox.addLayout(hboxA)
        vParentBox.addLayout(hboxC)
        vParentBox.addLayout(hboxD)
        #---------------------------自身widgetに親layoutを追加---------------------------
        self.setLayout(vParentBox)
        self.mainWidget = QWidget(self)
        self.mainWidget.setLayout(vParentBox)

        #---------------------------widgetに追加するメソッド---------------------------
    def execution_button(self):
        self.file_path_list =[]
        for i in range(self.listView.model().rowCount()):
            self.file_path_list.append(self.listView.model().item(i).text())
        self.loop_checker.main(self.file_type,self.file_path_list)
    
    def CallbackRadioButton(self,button=None):
        self.file_type = button.text()
    
        #---------------------------初期設定関連---------------------------
    def iniFileSetting(self,DirPath,fileName):
        iniFilePath = os.path.join(DirPath,fileName).replace("\\","/")
        self.iniFile = QSettings(iniFilePath,QSettings.IniFormat)

    def saveSettings(self):
        self.iniFile.setValue("geometry", self.saveGeometry())
        #self.iniFile.setValue(self.qlineA.objectName(), self.qlineA.text())
    
    def loadSettings(self):
        try:
            # if self.iniFile.value(self.qlineA.objectName()) == None:
            #     self.qlineA.setText("Test")
            # else:
            #     self.qlineA.setText(self.iniFile.value(self.qlineA.objectName()))            
            self.restoreGeometry(self.iniFile.value("geometry"))
        #Pyside2 version5.12.5 のエラー→PySide2.QtCore.QSettings.valueは、値が0の場合にNoneを返す
        # #INIファイルがない場合＋上記エラーの対応
        except TypeError:
            # self.qlineA.setText("Test")
            #restoreGeo は INIファイルがなくても使用できる(?)
            self.restoreGeometry(self.iniFile.value("geometry"))

    #仮想関数
    def closeEvent(self, event):
        self.saveSettings()

class ListView(QListView):
    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
        self.setDragEnabled(False)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        size = self.size()

        #icon処理
        self.folderPath = os.path.join(os.path.dirname(__file__),"DD_icon.png").replace("\\","/")

        self.setStyleSheet("""
            background-color :#2c2c2c;
            background-image: url({});
            background-repeat: no-repeat;
            background-position: center;
            """.format(self.folderPath)
        );
    
    def clearList(self):
        self.model().clear()
        self.setStyleSheet("""
            background-color :#2c2c2c;
            background-image: url({});
            background-repeat: no-repeat;
            background-position: center;
            """.format(self.folderPath)
        );
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ListView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ListView, self).dragMoveEvent(event)
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.setStyleSheet("""
            background-color :#2c2c2c;
            """.format(folderPath)
            );
            model = self.model()
            urls = event.mimeData().urls()
            for url in urls:
                filename = url.toLocalFile()
                #print(type(url))
                item = QStandardItem(filename)
                model.appendRow(item)
            event.accept()
        else:
            super(ListView, self).dropEvent(event)

def closeWindow(wname):
    widgets = QApplication.allWidgets()
    for w in widgets:
        if w.objectName() == wname:
            w.close()
            w.deleteLater()

def main():
    global Example_UI_ex
    app = QApplication.instance()
    closeWindow(WindowObjName)
    Example_UI_ex = MainWindow(parent)
    Example_UI_ex.show()