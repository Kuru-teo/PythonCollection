# -*- coding:utf-8 -*-
import os
import glob
import sys

from .MyPyside2Lib import MyPyside2Lib
try:
    import importlib
    importlib.reload(MyPyside2Lib)
except:
    #python2.x系対応
    reload(MyPyside2Lib)
from .MyPyside2Lib.MyPyside2Lib import *
#---------------------------mayaのTopWindow取得---------------------------
import maya.cmds as cmds
from maya import OpenMayaUI
from maya.app.renderSetup.model import *

try:
   import shiboken
except:
   import shiboken2 as shiboken

ptr = OpenMayaUI.MQtUtil.mainWindow()
parent = shiboken.wrapInstance(int(ptr), QWidget)

#--------------------------グローバル変数-------------------------------------
WindowObjName = "ChangeMatByRenderSetUp"
folderPath = os.path.dirname(__file__)
iniFileName = "UIsetting_ChangeMatByRenderSetUp"

#render setupに加えるレイヤー名
rsLayerName = "mm_ChangeMatLayer"
#作成するマテリアルのshadertype hlslかglsl等
materialNodeType = "dx11Shader"
#override対象のマテリアルのshadertype
overMaterialNodeType =["lambert","phong"]

#エラーメッセージ集
ErrorMessage_NoOverrrideMat = ""
ErrorMessage_NoTargetList = "No List"
ErrorMessage_NoRenderSetupLayer = ""

class uiWidget(QWidget):
    def __init__(self):
        super(uiWidget, self).__init__()
        self.settingUI()
    
    def settingUI(self):
        #---------------------------子layoutにWidgetの追加---------------------------
        #----------1段目
        hboxTitle = QHBoxLayout()
        vboxTitle = QVBoxLayout()
        
        self.Hborder = HorizontalLine()
        self.Hborder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vboxTitle.addWidget(self.Hborder)

        #レイアウト追加
        hboxTitle.addLayout(vboxTitle)

        #----------2段目
        hboxA = QHBoxLayout()

        layA = QVBoxLayout()
        layA.setContentsMargins(20, 20, 20, 20)

        #コンボボックス
        self.comboboxA = QComboBox(self)
        self.comboboxA.setObjectName("mm_override_material")
        layA.addWidget(self.comboboxA)

        #グループボックス
        self.groupboxA = QGroupBox("override material preset")
        self.groupboxA.setLayout(layA)

        #レイアウト追加
        hboxA.addWidget(self.groupboxA)

        #----------3段目
        hboxB = QHBoxLayout()
        layB = QHBoxLayout()

        #ボタン付きアイテムリスト
        list
        self.listWidgetA = listWidgetWithButton(["transform"])
        layB.addWidget(self.listWidgetA)

        #グループボックス
        self.groupboxC = QGroupBox("Target Object")
        self.groupboxC.setLayout(layB)

        #レイアウト追加
        hboxB.addWidget(self.groupboxC)

        #----------4段目
        hboxC = QHBoxLayout()
        layC = QHBoxLayout()
        
        #ボタン付きアイテムリスト
        self.listWidgetB = listWidgetWithButton(overMaterialNodeType)
        layC.addWidget(self.listWidgetB)

        #グループボックス
        self.groupboxE = QGroupBox("Target Material")
        self.groupboxE.setLayout(layC)

        #レイアウト追加
        hboxC.addWidget(self.groupboxE)

        #----------5段目
        hboxD = QHBoxLayout()
        layE = QHBoxLayout()
        #ボタン
        self.buttonC = DraggableButton("render setup")
        self.buttonC.setObjectName("mm_render_setup")
        self.buttonC.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        layE.addWidget(self.buttonC)

        #グループボックス
        self.groupboxB = QGroupBox("Render Setup")
        self.groupboxB.setLayout(layE)

        #レイアウト追加
        hboxD.addWidget(self.groupboxB)

        #----------6段目
        hboxE = QHBoxLayout()
        layD = QHBoxLayout()
        #ボタン
        self.buttonE = DraggableButton("switch material : True")
        self.buttonE.setObjectName("mm_override_material")
        self.buttonE.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        layD.addWidget(self.buttonE)

        #グループボックス
        self.groupboxD = QGroupBox("switch overrride material")
        self.groupboxD.setLayout(layD)

        #レイアウト追加
        hboxE.addWidget(self.groupboxD)

        #----------7段目
        hboxF = QHBoxLayout()
        self.buttonD = QPushButton("RESET")
        self.buttonD.setFixedHeight(20)
        self.buttonD.setObjectName("mm_button_close")
        hboxF.addWidget(self.buttonD)

        #----------spacer
        self.spaceA = QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        #---------------------------親layoutに子layoutを追加---------------------------
        vParentBox = QVBoxLayout()
        vParentBox.setContentsMargins(20,10,20,0)
        vParentBox.addLayout(hboxTitle)
        vParentBox.addLayout(hboxA)
        vParentBox.addLayout(hboxB)
        vParentBox.addLayout(hboxC)
        vParentBox.addLayout(hboxD)
        vParentBox.addLayout(hboxE)
        vParentBox.addSpacerItem(self.spaceA)
        vParentBox.addLayout(hboxF)
        #---------------------------自身widgetに親layoutを追加---------------------------
        self.setLayout(vParentBox)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.shaderPathList,self.shaderNameList = loadMaterialFiles(folderPath)
        self.targetMatList = []
        self.targetMeshList =[]
        self.rs = renderSetup.instance()
        self.visiable = True
        self.setWindowFlags(Qt.Dialog)

        #UI読み込み
        self.buildUI()
        #ステータスバーの作成
        statusBar = self.statusBar()
        #INIファイルの設定・読み込み
        self.iniFileSetting(folderPath,iniFileName)
        self.loadSettings()
        #現在comboboxで選択されているshader
        self.currentShaderIndex = self.cWidget.comboboxA.currentIndex()

    def buildUI(self):
        #Window基本情報
        self.setObjectName(WindowObjName)
        self.setGeometry(400, 400, 650, 600)
        self.resize(400,600)
        self.setWindowTitle(WindowObjName)
        #Windowにwidgetを追加
        #.uiで読み込んだ場合もここ
        self.cWidget = uiWidget()
        self.setCentralWidget(self.cWidget)
        #各Widgetのリスト
        self.listButton = self.getGuiWidgetByType(QPushButton)
        self.listCombobox = self.getGuiWidgetByType(QComboBox)
        self.listListWidgetWithButton = self.getGuiWidgetByType(listWidgetWithButton)
        self.listListWidget = self.getGuiWidgetByType(QListWidget)
        #各Widgetに関数を接続
        self.__setButtonGUI()
        self.__setComboboxGUI()
        self.__setlistWidgetWithButtonGUI()
    
    #---------------------------各Widgetに関数を接続---------------------------
    #各Wiggetと関数はWidgetのobjectNameで接続
    def __setButtonGUI(self):      
        for button in self.listButton:
            if button.objectName() == "mm_button_close":
                button.clicked.connect(self.resetTool)
            if button.objectName() == "mm_render_setup":
                button.clicked.connect(self.__renderSetup)
            if button.objectName() == "mm_override_material":
                button.clicked.connect(
                    lambda ignore=True, x=button: self.__switchMaterial(x))
    
    def __setComboboxGUI(self):
        for combobox in self.listCombobox:
            if combobox.objectName() == "mm_override_material":
                for mat in self.shaderNameList:
                    combobox.addItem(mat)
                    combobox.setCurrentIndex(0)
                combobox.currentIndexChanged.connect(self.CallbackConbobox)

    def __setlistWidgetWithButtonGUI(self):
        for lwb in self.listListWidgetWithButton:
            #このlamba式の書き方だと引数を作成時のものに固定できる
            if lwb.objectName() == "mm_listWidgetWithButton":
                lwb.buttonA.clicked.connect(lambda
                    x=lwb.listWidget, y=lwb.nodeType, z=True:
                    self.CallbackListWidgetButton(x, y, z))
                lwb.buttonB.clicked.connect(lambda
                    x=lwb.listWidget, y=lwb.nodeType, z=False:
                    self.CallbackListWidgetButton(x, y, z))
    
    #自身Widgetの中に含まれるwidgetをtype指定で取得
    def getGuiWidgetByType(self, type):
        ui_name_list = []
        listWidgets = self.findChildren(type)
        for widget in listWidgets:
            ui_name_list.append(widget.objectName())
        return listWidgets

    #---------------------------Widgetに紐づける関数---------------------------
    def CallbackConbobox(self, signal):
        self.currentShaderIndex = signal
    
    #指定したタイプのインスタンスをlistWidgetに追加・削除
    #引数は(対象のQlistWidget,対象のノードタイプ,追加ボタンor削除ボタン)
    def CallbackListWidgetButton(self, listWidget, type, isAdd):
        #addButtonの処理
        if isAdd == True:
            geos = getNodeHierarchyList(type)
            if len(geos) ==0:
                print("type:{}のノードが選択階層に含まれていません".format(type))
                return
            else:
                for geo in geos:
                    #同名は追加しない
                    items = listWidget.findItems(geo, Qt.MatchExactly)
                    if len(items) != 0:
                        continue
                    listWidget.addItem(geo)
        #deleteButtonの処理
        if isAdd == False:
            row = None
            row = listWidget.currentRow()
            item = listWidget.takeItem(row)
            listWidget.removeItemWidget(item)
            del item

    def __renderSetup(self):
        for wl in self.listListWidget:
            if self.checkExistsWidgetList(wl):
                continue
            else:
                print(ErrorMessage_NoTargetList)
                return
        
        self.clearRenderSetupLayer()
        self.clearMaterial()

        #マテリアル作成
        self.createMaterial(self.shaderPathList[self.currentShaderIndex])     
        #インスタンスの再取得
        self.rs = renderSetup.instance()
        #レイヤーの作成
        CMLayer = self.rs.createRenderLayer(rsLayerName)
        #コレクションの作成
        transCollect = CMLayer.createCollection('mm_transform')
        shaderCollect = CMLayer.createCollection('mm_shader')
        #セレクターの作成
        transSelector = transCollect.getSelector()
        transSelector.setFilterType(selector.Filters.kTransforms)
        shaderSelector = shaderCollect.getSelector()
        shaderSelector.setFilterType(selector.Filters.kShadingEngines)
        #コレクションに要素の追加
        for lwb in self.listListWidgetWithButton:
            if "transform" in lwb.nodeType:
                for i in range(0,lwb.listWidget.count()):
                    item =[]
                    item.append(lwb.listWidget.item(i).text())
                    transSelector.staticSelection.add(item)
            if "lambert" in lwb.nodeType:
                for i in range(0, lwb.listWidget.count()):
                    item = []
                    itemName = lwb.listWidget.item(i).text()
                    #lambert1のみshadingEngineの名前が固定のため分岐
                    if itemName == "lambert1":
                        item.append("initialShadingGroup")
                    else:
                        item.append(lwb.listWidget.item(i).text()+"SG")
                    shaderSelector.staticSelection.add(item)
        #shderOverrideの作成
        override = shaderCollect.createOverride(
           self.shaderNameList[self.currentShaderIndex]+"SG", typeIDs.shaderOverride)
        override.setShader(
            self.shaderNameList[self.currentShaderIndex], '.outColor')

        #レイヤーのレンダリング設定
        self.rs.switchToLayer(CMLayer)

    def __switchMaterial(self,button):
        self.visiable = bool(1 - int(self.visiable))
        button.setText("switch material: {}".format(str(self.visiable)))
        #レイヤーを取得しにいく
        try:
            CMLayer = self.rs.getRenderLayer(rsLayerName)
        except:
            CMLayer =None
        
        if CMLayer != None:
            if self.visiable:
                self.rs.switchToLayer(CMLayer)
            else:
                self.rs.switchToLayer(self.rs.getDefaultRenderLayer())

    def resetTool(self):
        #ツール関連のレイヤー消す
        self.clearRenderSetupLayer()
        #ツール関連のマテリアルを消す
        self.clearMaterial()
        #ListWidgetを消す
        self.clearListWidget()

    def clearMaterial(self):
        allMaterials = cmds.ls(mat=True)
        for mat in allMaterials:
            if mat in self.shaderNameList:
                connectNode = cmds.listConnections(mat,d=False)
                cmds.delete(mat)
                cmds.delete(mat+"SG")
                #Shaderノードに接続されているノードも削除
                if connectNode != None:
                    for node in connectNode:
                        cmds.delete(node)
    
    def clearRenderSetupLayer(self):
        self.rs = renderSetup.instance()
        layers = self.rs.getRenderLayers()
        for layer in layers:
            if rsLayerName in layer.name():
                renderLayer.delete(layer)
    
    def clearListWidget(self):
        for lw in self.listListWidget:
            lw.clear()

    #マテリアル名はshaderファイル名です
    def createMaterial(self,shaderPath):
        nameBase = os.path.basename(shaderPath)
        name = os.path.splitext(nameBase)[0]
        shaderNode = cmds.shadingNode(materialNodeType, name=name, asShader=True)
        cmds.sets(name="%sSG" %shaderNode, empty=True, renderable=True, noSurfaceShader=True)
        cmds.setAttr("%s.shader" % shaderNode, shaderPath, type="string")
        cmds.connectAttr("%s.outColor" % shaderNode, "%sSG.surfaceShader" % shaderNode)

    def checkExistsWidgetList(self,widgetList):
        if widgetList.count() == 0:
            return False
        else:
            return True

    def checkExistsNode(self,name,nodes):
        return
    
    def getAllNodeByType(self,type):
        topNode = cmds.ls(selection=True, dag=True)
        allNodes = None        
    
    #---------------------------初期設定関連---------------------------
    def iniFileSetting(self,DirPath,fileName):
        iniFilePath = os.path.join(DirPath,fileName)
        self.iniFile = QSettings(iniFilePath,QSettings.IniFormat)

    def saveSettings(self):
        self.iniFile.setValue("geometry", self.saveGeometry())
        self.iniFile.setValue(self.cWidget.comboboxA.objectName(
        ), self.cWidget.comboboxA.currentIndex())
    
    def loadSettings(self):
        try:
            self.cWidget.comboboxA.setCurrentIndex(int(self.iniFile.value
            (self.cWidget.comboboxA.objectName())))
            self.restoreGeometry(self.iniFile.value("geometry"))
         #Pyside2 version5.12.5 のエラー→PySide2.QtCore.QSettings.valueは、値が0の場合にNoneを返す
         #INIファイルがない場合＋上記エラーの対応
        except TypeError:
            self.cWidget.comboboxA.setCurrentIndex(0)
            #restoreGeo は INIファイルがなくても使用できる(?)
            self.restoreGeometry(self.iniFile.value("geometry"))

    #---------------------------仮想関数---------------------------
    def closeEvent(self, event):
        self.saveSettings()

#---------------------------汎用関数---------------------------
#選択したノード以下の階層から指定したtypeのインスタンスをlistで返す
def getNodeHierarchyList(type):
    ##選択階層以下のジオメトリの指定ノードを取得
    cmds.select(hi=True)
    nodes = cmds.ls(sl=True, type=type, tr=True)
    for node in nodes[:]:
        if cmds.nodeType(node) in type:
            pass
        else:
            nodes.remove(node)
    cmds.select(nodes)
    return nodes

def closeWindow(wname):
    widgets = QApplication.allWidgets()
    for w in widgets:
         if w.objectName() == wname:
             w.close()
             w.deleteLater()

def loadMaterialFiles(folderDir):
    try:
        matFolder = os.path.join(folderDir, "maya_materials", "*.fx")
        shaderPathList =[]
        shaderNameList =[]
        shaderPathList = glob.glob(matFolder)
        for path in shaderPathList:
            fileBaseName = os.path.basename(path)
            fileName = os.path.splitext(fileBaseName)[0]
            shaderNameList.append(fileName)
        return shaderPathList,shaderNameList
    except:
        pass

#---------------------------以下DCCツールごとのルールに沿って編集---------------------------
#mayaの場合
def main():
    global Example_UI_ex
    app = QApplication.instance()
    closeWindow(WindowObjName)
    Example_UI_ex = MainWindow(parent)
    Example_UI_ex.show()
    sys.exit()
    app.exec_()