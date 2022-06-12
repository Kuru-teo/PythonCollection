# -*- coding:utf-8 -*-

from MyPyside2Lib.MyPyside2Lib import *
import os
import glob
import time

WindowObjName = "mm_test_window"
folderPath = os.getcwd()
iniFileName = "UIsetting_MyPyside2"
#colorDict = {"色":[MainColor,SubColor,BG_MainColor,BG_SubColor,GP_BorderColor]}
colorDict = {"Green": ["#027373", "#038C7F", "#A9D9D0", "#F2E7DC", "#FFF9F5"],
             "Yellow": ["#BF8845", "#F2A341", "#4C594E", "#BF8845", "#F2DCB3"],
             "Purole": ["#C899F7", "#EE8BF0", "#9896E0", "#99C4F7", "#86E7F0"],
             "night": ["#B4BEC9", "#DEEFE7", "#202022", "#878787", "#CACACA"]}

class uiWidget(QWidget):
    def __init__(self):
        super(uiWidget, self).__init__()
        self.settingUI()
    
    def settingUI(self):
        #---------------------------子layoutにWidgetの追加---------------------------
        #----------一段目
        hboxTitle = QHBoxLayout()
        vboxTitle = QVBoxLayout()
        #タイトル
        self.labelTitle = QLabel("Utility Widget")
        self.labelTitle.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.labelTitle.setAlignment( Qt.AlignCenter)
        self.labelTitle.setObjectName("Header")
        vboxTitle.addWidget(self.labelTitle)
        vboxTitle.setAlignment(Qt.AlignHCenter)

        #画像
        self.ImageA = ImageLabel(os.path.join(
            folderPath, "resource", "gear_L.png"))
        self.ImageA.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ImageB = ImageLabel(os.path.join(
            folderPath, "resource", "gear_R.png"))
        self.ImageB.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        #レイアウト追加
        hboxTitle.addWidget(self.ImageA)
        hboxTitle.addLayout(vboxTitle)
        hboxTitle.addWidget(self.ImageB)
        hboxTitle.setAlignment(Qt.AlignHCenter)
        hboxTitle.setSpacing(20)

        #----------二段目
        hboxA = QHBoxLayout()

        layA = QVBoxLayout()
        layA.setContentsMargins(20, 20, 20, 20)
        layB = QVBoxLayout()
        layB.setContentsMargins(20, 20, 20, 20)
        layC = QVBoxLayout()
        layC.setContentsMargins(20, 20, 20, 20)

        #ボタン
        self.buttonA = DraggableButton("Button A")
        self.buttonA.setObjectName("mm_button_message")
        self.buttonA.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        layA.addWidget(self.buttonA)

        #トグル
        self.toggleA = PyToggle()
        self.toggleA.setObjectName("mm_toggleA")
        #self.buttonB.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        layB.addWidget(self.toggleA)
        layB.setAlignment(Qt.AlignHCenter)

        #コンボボックス
        self.comboboxA = QComboBox(self)
        colorDictKeys = list(colorDict.keys())
        for Key in colorDictKeys:
            self.comboboxA.addItem(Key)
        self.comboboxA.setObjectName("mm_ComboBoxA")
        layC.addWidget(self.comboboxA)

        #グループボックス
        self.groupboxA = QGroupBox("QMessageBox")
        self.groupboxA.setLayout(layA)
        self.groupboxB = QGroupBox("QCheckBox")
        self.groupboxB.setLayout(layB)
        self.groupboxC = QGroupBox("QComboBox")
        self.groupboxC.setLayout(layC)

        #レイアウト追加
        hboxA.addWidget(self.groupboxA)
        hboxA.addWidget(self.groupboxB)
        hboxA.addWidget(self.groupboxC)

        #----------三段目
        hboxB = QHBoxLayout()

        layD = QVBoxLayout()
        layD.setContentsMargins(20, 20, 20, 20)
        layE = QVBoxLayout()
        layE.setContentsMargins(20, 20, 20, 20)
        layF = QVBoxLayout()
        layF.setContentsMargins(20, 20, 20, 20)

        font = QFont()
        font.setFamily("Helvetica")
        font.setBold(True)
        font.setWeight(100)
        font.setPointSize(30)

        #スクロールバー
        FloatSlider.labelName = "SliderA"
        self.sliderA = FloatSlider()
        self.sliderA.setObjectName("mm_SliderA")
        layD.addWidget(self.sliderA)

        #プログレスバー用ボタン
        self.buttonB = DraggableButton("calculate")
        self.buttonB.setObjectName("mm_button_progress")
        self.buttonB.setFixedSize(100,50)
        layE.addWidget(self.buttonB)
        layE.setAlignment(Qt.AlignHCenter)

        #ラベル
        self.labelC = QLabel("C")
        #self.labelC.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.labelC.setAlignment(Qt.AlignCenter)
        layF.addWidget(self.labelC)

        #グループボックス
        self.groupboxD = QGroupBox("QAbstractSlider")
        self.groupboxD.setLayout(layD)
        self.groupboxE = QGroupBox("QProgressDialog")
        self.groupboxE.setLayout(layE)
        self.groupboxF = QGroupBox("GroupC")
        self.groupboxF.setLayout(layF)

        #レイアウト追加
        hboxB.addWidget(self.groupboxD)
        hboxB.addWidget(self.groupboxE)
        #hboxB.addWidget(self.groupboxF)

        #----------四段目
        hboxC = QHBoxLayout()
        self.buttonD = QPushButton("Close")
        self.buttonD.setFixedHeight(20)
        self.buttonD.setObjectName("mm_button_close")
        #self.buttonD.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        hboxC.addWidget(self.buttonD)

        #----------spacer
        self.spaceA = QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.spaceB = QSpacerItem(0, 20, QSizePolicy.Expanding)
        
        #---------------------------親layoutに子layoutを追加---------------------------
        vboxA = QVBoxLayout()
        vboxA.setContentsMargins(20,10,20,0)
        vboxA.addLayout(hboxTitle)
        vboxA.addSpacerItem(self.spaceA)
        vboxA.addLayout(hboxA)
        vboxA.addLayout(hboxB)
        vboxA.addSpacerItem(self.spaceB)
        vboxA.addLayout(hboxC)
        #print(self.labelA.sizePolicy())
        #print(hboxA.sizeHint())
        #print(hboxC.geometry())
        #---------------------------自身widgetに親layoutを追加---------------------------
        self.setLayout(vboxA)

class MainWindow(WindowBase):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.buildUI()
        #INIファイルの設定・読み込み
        self.iniFileSetting(folderPath,iniFileName)
        self.loadSettings()
        #テーマカラーを指定するコンボボックスを指定
        self.themeColor_cmb = self.cWidget.comboboxA
        #現在のテーマカラー
        self.colorPreset = None
        self.colorPreset = list(colorDict.keys())[self.themeColor_cmb.currentIndex()]
        #Widgetの色上書き
        self.setColor(self.colorPreset)
    
    def buildUI(self):
        #Window基本情報
        self.setObjectName(WindowObjName)
        self.setGeometry(400, 400, 650, 300)       
        #Windowにwidgetを追加
        #.uiで読み込んだ場合もここ
        self.cWidget = uiWidget()
        self.setCentralWidget(self.cWidget)
        #各Widgetのリスト
        self.listButton = self.getGuiWidgetByType(QPushButton)
        self.listCombobox = self.getGuiWidgetByType(QComboBox)
        self.listCheckbox = self.getGuiWidgetByType(QCheckBox)
        self.listSlider = self.getGuiWidgetByType(QAbstractSlider)
        self.listLabel = self.getGuiWidgetByType(QLabel)
        self.listGroupBox = self.getGuiWidgetByType(QGroupBox)
        #各Widgetに関数を接続
        self.setButtonGUI()
        self.setComboboxGUI()
        self.setCheckboxGUI()
        self.setSliderGUI()
    
    #---------------------------各Widgetに関数を接続---------------------------
    #各Wiggetと関数はWidgetのobjectNameで接続
    def setButtonGUI(self):      
        for button in self.listButton:
            if button.objectName() == "mm_button_close":
                button.clicked.connect(lambda: closeWindow(WindowObjName))
            if button.objectName() == "mm_button_message":
                button.clicked.connect(lambda: self.showMessageBox("Message Box",False))
            if button.objectName() == "mm_button_progress":
                button.clicked.connect(self.showProgressDialog)
    
    def setComboboxGUI(self):
        for combobox in self.listCombobox:
            if combobox.objectName() == "mm_ComboBoxA":
                combobox.currentIndexChanged[str].connect(self.setColor)

    def setCheckboxGUI(self):
        for checkbox in self.listCheckbox:
            if checkbox.objectName() == "mm_toggleA":
                checkbox.stateChanged.connect(
                    lambda: self.__setNightMode(checkbox))

    def setSliderGUI(self):
        for slider in self.listSlider:
            if slider.objectName() == "mm_SliderA":
                slider.valueChanged.connect(self.setColorValue)

    def getGuiWidgetByType(self, type):
        ui_name_list = []
        #自身Widgetの中に含まれるwidgetをtype指定で取得
        listWidgets = self.findChildren(type)
        for widget in listWidgets:
            ui_name_list.append(widget.objectName())
        return listWidgets

    #---------------------------色替え部分の指定---------------------------
    #ウィンドウはQPainterのsetBrush(self.gradient)で色付けしている前提
    def setWindowColor(self,colList,win):
        win.gradient = QLinearGradient(
            QRectF(win.rect()).bottomLeft(), QRectF(win.rect()).topLeft())
        win.gradient.setColorAt(1.0, colList[2])
        win.gradient.setColorAt(0.0, colList[3])
        #ボーダーがあれば色替え
        try:
            pass
        except:
            pass
    
    def setButtonColor(self, colList):
        #format使えない？
        col = """QPushButton{ background-color: %s;}
                 QPushButton:hover{ background-color: %s;}
                 QPushButton:pressed{ color: %s;}""" % (
            colList[0], colList[1], colList[2])
        for button in self.listButton:
            button.setStyleSheet(col)
    
    def setLabelColor(self, colList):
        col = """QLabel#Header{ border-color: %s;}""" % (
            colList[0])
        for label in self.listLabel:
            label.setStyleSheet(col)

    def setToggleColor(self, colList):
        pass

    def setComboboxColor(self, colList):
        col = """QComboBox{ border-color: %s;}
                 QComboBox{ background-color: %s;}
                 QComboBox QAbstractItemView { background-color: %s;
                 selection-background-color: %s;}""" % (
            colList[0], colList[2], colList[2], colList[1])
        for combobox in self.listCombobox:
            combobox.setStyleSheet(col)

    def setSliderColor(self, colList):
        col = """QSlider:handle {background: %s;}
                 QSlider:handle:pressed{background: %s;}
                 QSlider:sub-page{background: %s;}""" % (
            colList[2], colList[0], colList[1])
        for slider in self.listSlider:
            slider.setStyleSheet(col)

    def setGroupColor(self, colList):
        #色のみ指定の方法がない?
        col = """QGroupBox{border: 3px solid %s;
                 color: %s}""" % (colList[4], colList[4])
        for groupbox in self.listGroupBox:
            groupbox.setStyleSheet(col)

    #---------------------------Widgetに紐づける関数---------------------------
    #自身Widget内の各ウィジェットを色替え
    def setColor(self, colorPreset):
        self.setButtonColor(colorDict[colorPreset])
        self.setLabelColor(colorDict[colorPreset])
        self.setComboboxColor(colorDict[colorPreset])
        self.setSliderColor(colorDict[colorPreset])
        self.setToggleColor(colorDict[colorPreset])
        self.setGroupColor(colorDict[colorPreset])
        self.setWindowColor(colorDict[colorPreset],self)
        self.update()
        self.colorPreset = colorPreset
    
    def setColorValue(self,signal):
        pass
        #print(signal)

    def __setNightMode(self,toggle):
        if toggle.isChecked():
            self.setColor("night")
            self.themeColor_cmb.setEnabled(False)
        else:
            self.themeColor_cmb.setEnabled(True)
            self.setColor(self.themeColor_cmb.currentText())
    
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
        except:
            pass
    
    #---------------------------ダイアログ---------------------------
    def showMessageBox(self,text,accept:bool):
        msgBox = MessageBoxBase()
        msgBox.setText(text)
        if not accept:
            yesButton = msgBox.addButton(QMessageBox.Yes)
            noButton = msgBox.addButton(QMessageBox.No)     
        self.setWindowColor(colorDict[self.colorPreset],msgBox)
        msgBox.exec_()
    
    def showProgressDialog(self):
        max = 100
        cancelflag = False
        progressDialog = ProgressDialogBase(
            "Progress...", "Cancel", 0, max, self, Qt.FramelessWindowHint)
        progressDialog.setWindowTitle("Progress Dialog")
        #色替え
        col = """QProgressDialog{ background-color: %s;}""" % (
            colorDict[self.colorPreset][0])
        progressDialog.setStyleSheet(col)
        progressDialog.show()
        for count in range(max+1):
            qApp.processEvents()
            if progressDialog.wasCanceled():
                cancelflag = True
                break
            progressDialog.setValue(count)
            progressDialog.setLabelText("Progress... %d %%" % count)
            time.sleep(0.01)
        if cancelflag == False:
            self.showMessageBox("Finish Process", True)

    #---------------------------仮想関数---------------------------
    def closeEvent(self, event):
        super(MainWindow, self).closeEvent(event)
        self.saveSettings()

#---------------------------汎用関数---------------------------
def closeWindow(wname):
    widgets = QApplication.allWidgets()
    for w in widgets:
         if w.objectName() == wname:
             w.close()
             w.deleteLater()

#ファイル名は[qssLib_〇〇]で決め打ち
#同じセレクタがあった場合は後発に上書きされるので気を付ける
def loadQSSFiles(folderDir):
    try:
        qssFolder = os.path.join(folderDir, "qssLib")
        os.chdir(qssFolder)
        styleList = []
        for qssfile in glob.glob("qssLib_*.qss"):
            with open(qssfile,"r") as f:   
                styleList.append(f.read())
        styleData = "\n".join(styleList)
        return styleData
    except:
        style = ""

#---------------------------以下DCCツールごとのルールに沿って編集---------------------------
def main(cur):
    #closeWindow(cur)
    #mayaWindow =  shiboken2.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QWidget)
    #winA = MainWindow(mayaWindow)
    #winA = MainWindow()
    #winA.show()
    pass

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # load qss files
    style = loadQSSFiles(folderPath)
    app.setStyleSheet(style)
    # close window
    closeWindow(WindowObjName)
    # Create and show the form
    winA = MainWindow()
    winA.show()
    # Run the main Qt loop
    sys.exit(app.exec_())




