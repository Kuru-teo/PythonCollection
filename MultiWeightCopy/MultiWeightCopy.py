# -*- coding: utf-8 -*-

###############
"""
■MultiWeightCopyBySameNameとは
コピー元のジオメトリリストから、同名のコピー先のジオメトリリストにウエイトをまとめてコピーするツールです。
コピー元のジオメトリにはウエイトが必要ですが、
コピー先のジオメトリにウエイトをバインドしておく必要はありません（ヒストリを削除しておいてください)

■使い方
➀コピー元のジオメトリを選択し、「Source Mesh」ボタンを押します
　（複数のジオメトリを含んだ一番上のトランスフォームノード一つだけ選択でも大丈夫です)
➁コピー先のジオメトリを選択し、「Target Mesh」ボタンを押します
➂「Copy」のボタンを押すと、同名のジオメトリの組み合わせでSourceMeshからTargetMeshにウエイトがコピーされます。

"""
##    [免責事項]
##        本ツール、コードを使用したことによって
##        引き起こるいかなる損害も当方は一切責任を負いかねます。
##        自己責任でご使用ください。
###############

######----------モジュールのインポート
import maya.cmds as cmds
import shiboken2

from maya import OpenMayaUI
from maya.app.general import mayaMixin
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

######----------メッセージ集
ListName_source = "the Source Mesh list."
Listname_copy = "the Target Mesh list."

ErrorMessage_sameName = "Geometry with the same name cannot be selected"
ErrorMessage_noselect = "Geometry is not selected."
ErrorMessage_existingskin = "There are sikned geometries in "
ErrorMessage_req_deleteHistory = "Please delete history."
ErrorMessage_req_bind_skin = "Please bind skin."
ErrorMessage_nonskin = "There are non sikned geometries in "
ErrorMessage_notCopy = "Copying canceled."

CompletedMessage = "Copying completed."

######----------メインGUIクラス
class MWC_GUI(mayaMixin.MayaQWidgetBaseMixin,QWidget):
    def __init__(self, parent = None):
        super(MWC_GUI, self).__init__(parent)
        self.closeExistWindow()
        self.initGUI()
    
    def closeExistWindow(self):
        #親クラスオブジェクトの取得(mayaのメインウィンドウ)
        mainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(mainWindowPtr),QWidget)

        child_list =  parent.children()
        for c in child_list:
             if self.__class__.__name__ == c.__class__.__name__:
                 c.close()

    def initGUI(self):
        ####
        #ウインドウ設定
        self.setGeometry(500, 300, 500, 500)
        self.setWindowTitle("MultiWeightCopyBySameName")
        #大枠のレイアウト
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        #ボタン用関数のインスタンス
        BtF = BtFunc()
        mainLayout.addWidget(self._makeHorizontalLine())
        mainLayout.addWidget(self._makeHorizontalLine())
        
        ####--------------------------------------一段目のレイアウト--------------------------------------####
        buttonSourceMesh = QPushButton("Source Mesh")
        tableSource = QTableWidget()
        tableSource.setEditTriggers(QTableWidget.NoEditTriggers)
        textSource = QLabel()
        transformSourceList = []
        buttonCopyMesh = QPushButton("Target Mesh")
        tableCopy = QTableWidget()
        tableCopy.setEditTriggers(QTableWidget.NoEditTriggers)
        textCopy = QLabel()
        transformCopyList = []

        buttonSourceMesh.clicked.connect(lambda x=tableSource, y=transformSourceList: BtF.UpdateTable(x,y))
        buttonCopyMesh.clicked.connect(lambda x=tableCopy, y=transformCopyList: BtF.UpdateTable(x,y))
        textSource.setText("you need to select skined mesh.\n")
        textSource.setMaximumSize(200,50)
        textCopy.setText("you need to select mesh that was \ndeleted history.")
        textCopy.setMaximumSize(200,50)

        SRL_FirstcolumLayout = QVBoxLayout()
        SRL_FirstcolumLayout.addWidget(buttonSourceMesh)
        SRL_FirstcolumLayout.addWidget(textSource)
        SRL_FirstcolumLayout.addWidget(tableSource)
        SRL_SecondcolumLayout = QVBoxLayout()
        SRL_SecondcolumLayout.addWidget(buttonCopyMesh)
        SRL_SecondcolumLayout.addWidget(textCopy)
        SRL_SecondcolumLayout.addWidget(tableCopy)
        SecondRowLayout = QHBoxLayout()
        SecondRowLayout.addLayout(SRL_FirstcolumLayout)
        SecondRowLayout.addLayout(SRL_SecondcolumLayout)

        mainLayout.addLayout(SecondRowLayout)
        mainLayout.addWidget(self._makeHorizontalLine())
        
        ####--------------------------------------二段目のレイアウト--------------------------------------####
        buttonWeightCopy = QPushButton("Copy")

        buttonWeightCopy.clicked.connect(lambda x=transformSourceList, y=transformCopyList, z=tableSource, w=tableCopy: BtF.mulCopyWeight(x,y,z,w))
        ThirdRowLayout = QHBoxLayout()
        ThirdRowLayout.addWidget(buttonWeightCopy)
        mainLayout.addLayout(ThirdRowLayout)

    ##区切りの線のためのウィジェット
    def _makeHorizontalLine(self):
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        return hline


######----------Buttonの中身（関数)クラス
class BtFunc:
    ##インスタンス変数
    Errormesh = []
    
    def __init__(self):
        self.MYDialog = Dialogs()

    ####選択階層以下のジオメトリでGUIのテーブルを更新する関数
    def UpdateTable(self,table,list):
        ##選択階層以下のジオメトリのトランスフォームノードを取得
        cmds.select(hi=True)
        geometry = cmds.ls(sl = True, geometry=True)
        #フラグ path は、同名のオブジェクトを取得する際にパスにしてくれる
        transforms = cmds.listRelatives(geometry, p=True, path=True, type = "transform")
        cmds.select(transforms, r=True)

        ##ジオメトリの名前だけ抽出しリスト化
        geoName = []
        for trans in transforms:
            name = (trans.split("|")[-1:])[0]
            geoName.append(name)

        ##ジオメトリリストの中に重複した名前があると関数停止
        if self.detectOverlapping(geoName):
            self.MYDialog.showErrorDialog(ErrorMessage_sameName)
            return
            
        ##問題なければトランスフォームノードをリストに登録
        del list[:]
        list.extend(transforms)

        ##QTableWidgetに表示名を登録
        #ジオメトリ名の行番号とそのジオメトリのトランスフォームノードのリスト番号は一致している
        table.setRowCount(len(geoName))
        table.setColumnCount(1)
        table.horizontalHeader().setVisible(False)
        for index, gn in enumerate(geoName):
            item= QTableWidgetItem(gn)
            table.setItem(index-1, 1, item)

    ####コピー元リストとコピー先リストでウエイトをコピーする関数
    def mulCopyWeight(self,sourceTransforms,copyTransforms,sourcetable,copytable):
        ##sourceTransforms,copyTransformsがからではないかをチェック
        if not sourceTransforms:
            self.MYDialog.showErrorDialog(ErrorMessage_noselect)
            return
        if not copyTransforms:
            self.MYDialog.showErrorDialog(ErrorMessage_noselect)
            return
        ##sourceTransformsにバインドされていないメッシュがないかをチェック
        STskin,STnonskin = self.detectSkinCluster(sourceTransforms)
        if STnonskin:
            errormesh = "<br>".join(STnonskin)
            self.MYDialog.showErrorDialog(ErrorMessage_nonskin + ListName_source + 
            ErrorMessage_req_bind_skin +"<br>" + "<br>"+errormesh)
            return
        ##copyTransformsにバインドされたメッシュがないかをチェック
        CTskin,CTnonskin = self.detectSkinCluster(copyTransforms)
        if CTskin:
            errormesh = "<br>".join(CTskin)
            self.MYDialog.showErrorDialog(ErrorMessage_existingskin + Listname_copy +
            ErrorMessage_req_deleteHistory+ "<br>" + "<br>"+errormesh)
            return

        ##一つのメッシュあたりのパーセンテージを計算(progressWindowのため)
        copyprogress = 100.0/len(sourceTransforms)
        self.MYDialog.showProgressDialog()
        ##キャンセルフラグ
        flag = False

        ##コピー元リストとコピー先リストで同じ名前があればその組み合わせでウエイトコピー
        for STindex in range(sourcetable.rowCount()):
            sourceGeoName = sourcetable.item(STindex,0).text()
            for CTindex in range(copytable.rowCount()):
                copyGeoname = copytable.item(CTindex,0).text()
                #progresswindowの更新
                qApp.processEvents()
                ##キャンセルボタンは多重ループの抜け出し
                if self.MYDialog.progressDialog.wasCanceled():
                    flag = True
                    break
                if sourceGeoName == copyGeoname:
                    self.mainCopy(sourceTransforms[STindex],copyTransforms[CTindex])
                #progresswindowのパーセンテージを進める
                self.MYDialog.progressDialog.setValue((STindex+1)*copyprogress)
            if flag:
                break
        
        ##コピー終了のダイアログ
        if flag:
            self.MYDialog.showFinishDialog(ErrorMessage_notCopy)
        else:
            self.MYDialog.showFinishDialog(CompletedMessage)

    ##-----------------------------------------------------------------------------------##
    ####リスト内の重複を検知する関数
    def detectOverlapping(self,list):
        overlapp = False
        if len(list) != len(set(list)):
            overlapp = True
        return overlapp
    
    ####リスト内のジオメトリがスキンクラスターを持っているかどうか検知する関数
    def detectSkinCluster(self,list):
        haveSkinGeos =[]
        notHaveSkinGeos =[]
        for trans in list:
            sourceShape = self.getShape(trans)
            histories = cmds.listHistory(sourceShape, pruneDagObjects=True, interestLevel=2)
            if histories is None:
                notHaveSkinGeos.append(trans)
            else:
                skinCluster = cmds.ls(histories, type="skinCluster")
                if skinCluster:
                    haveSkinGeos.append(trans)
                else:
                    notHaveSkinGeos.append(trans)
        return haveSkinGeos,notHaveSkinGeos

    ####ウエイトコピーのメインメソッド
    def mainCopy(self,sourceTransform,copyTransform):
        sourceShape = self.getShape(sourceTransform)
        sourceSkinCluster = self.getSkinCraster(sourceShape)
        copyInfluence = self.getInfluence(sourceSkinCluster,copyTransform)
        copySkincluster = self.bindSkin(copyInfluence)
        self.copyWeight(sourceSkinCluster,copySkincluster)

    ####「シェイプノード」を取得する関数
    def getShape(self,transform):
        shape = cmds.listRelatives(transform, shapes=True, noIntermediate=True,  path=True)[0]
        return shape
        
    ####「スキンクラスターノード」を取得する関数
    def getSkinCraster(self,shape):
        histories = cmds.listHistory(shape, pruneDagObjects=True, interestLevel=2)
        print(histories)
        sourceSkinCluster = cmds.ls(histories, type="skinCluster")[0]
        return sourceSkinCluster

    ####「インフルエンス」を取得する関数
    def getInfluence(self,skinCluster,transform):
        influences = cmds.skinCluster(skinCluster, q=True, influence=True)
        # influencesのリストの最後にCopy先のトランスフォームノードを追加する
        influences.append(transform)
        return influences

    ####スキンバインドする関数
    def bindSkin(self,influences):
        copySkinCluster = cmds.skinCluster(influences,toSelectedBones = True)
        copySkinCluster = copySkinCluster[0]
        return copySkinCluster
    
    ####ウエイトコピーする関数
    def copyWeight(self,sourceSkinCluster,copySkinCluster):
        cmds.copySkinWeights(
            sourceSkin = sourceSkinCluster,
            destinationSkin = copySkinCluster,
            noMirror=True,
            influenceAssociation="oneToOne",
            surfaceAssociation="closestPoint"
        )

######----------ダイアログクラス
class Dialogs(mayaMixin.MayaQWidgetBaseMixin,QDialog):
    def __init__(self, parent = None):
        super(Dialogs, self).__init__(parent)
        #エラーダイアログを常にトップに表示
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #エラーダイアログのインスタンス
        self.errorDialog = QErrorMessage(self)
    
    def showErrorDialog(self,message):
        self.errorDialog.showMessage(message)

    ####コピー完了のダイアログ関数
    def showFinishDialog(self,message):
        self.finishDialog = QMessageBox().about(None, "Info Message", message)
    
    ####コピー中のダイアログ関数
    def showProgressDialog(self):
        self.progressDialog = QProgressDialog("Progress...","Cancel",0,100,self)
        self.progressDialog.setWindowTitle("copy weight")
        self.progressDialog.show()

######----------main
def main():
    gui = MWC_GUI()
    gui.show()

if __name__ == '__main__':
    app = QApplication.instance()
    main()
    app.exec_()