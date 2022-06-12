from cmath import rect
from distutils.log import debug
import sys
import imp
import os
from MyPyside2Lib import imageResource

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

class WindowBase(QMainWindow):
    def __init__(self, parent=None):
        super(WindowBase, self).__init__(parent)
        self.__isDrag = False
        self.__startPos = QPoint(0, 0)
        self.gradient = Qt.red
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.borderRadius = 15
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        #ステータスバーの作成
        statusBar = self.statusBar()

    #---------------------------MouseEvent---------------------------
    def mousePressEvent(self, event):
        self.__isDrag = True
        self.__startPos = event.pos()
        super(WindowBase, self).mousePressEvent(event)
     
    def mouseReleaseEvent(self, event):
        self.__isDrag = False
        super(WindowBase, self).mouseReleaseEvent(event)
         
    def mouseMoveEvent(self, event):
        if self.__isDrag:
            self.move(self.mapToParent(event.pos() - self.__startPos))
        super(WindowBase, self).mouseMoveEvent(event)
        
    #---------------------------paint---------------------------
    def paintEvent(self, event):
        s = self.size()
        self.qp = QPainter()
        self.qp.begin(self)
        self.qp.setRenderHint(QPainter.Antialiasing, True)
        self.qp.setPen(Qt.NoPen)
        self.qp.setBrush(self.gradient)
        self.qp.drawRoundedRect(0, 0, s.width(), s.height(),
                                self.borderRadius, self.borderRadius)
        self.qp.end()

class MessageBoxBase(QMessageBox):
    def __init__(self, *args, **kwargs):
        super(MessageBoxBase, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.borderRadius = 15
        self.borderWidth = 3
        self.borderColor = Qt.white
        self.gradient = Qt.red
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.__isDrag = False
    
    #---------------------------MouseEvent---------------------------
    
    def mousePressEvent(self, event):
        self.__isDrag = True
        self.__startPos = event.pos()
        super(MessageBoxBase, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.__isDrag = False
        super(MessageBoxBase, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.__isDrag:
            self.move(self.mapToParent(event.pos() - self.__startPos))
        super(MessageBoxBase, self).mouseMoveEvent(event)

    #---------------------------paint---------------------------
    def paintEvent(self, event):
        s = self.size()
        self.qp = QPainter()
        self.qp.begin(self)
        self.qp.setRenderHint(QPainter.Antialiasing, True)
        self.qp.setPen(Qt.NoPen)
        self.qp.setBrush(self.borderColor)
        self.qp.drawRoundedRect(0, 0, s.width(), s.height(),
                                self.borderRadius, self.borderRadius)
        self.qp.setBrush(self.gradient)
        self.qp.drawRoundedRect(0+self.borderWidth, 0+self.borderWidth, s.width()-self.borderWidth*2, s.height()-self.borderWidth*2,
                                self.borderRadius*0.9, self.borderRadius*0.9)
        self.qp.end()

class ProgressDialogBase(QProgressDialog):
    def __init__(self, *args, **kwargs):
        super(ProgressDialogBase, self).__init__(*args, **kwargs)
    """
    def changeEvent(self, event):
        super(ProgressDialogBase, self).changeEvent(event)
        print("ooodddddddddddddddooooo")
    """

class AnimComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super(AnimComboBox, self).__init__(*args, **kwargs)
        
        self.ComboBox_ListView = QListView(self)
        self.ComboBox_ListView.setObjectName("ComboBox")
        self.ComboBox_ListView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

class FloatSlider(QAbstractSlider):
    valueChanged = Signal(float)
    labelName = ""
    min = 0.0
    max = 100.0
    __boost = 1

    def __init__(self, *args, **kwargs):
        super(FloatSlider, self).__init__(*args, **kwargs)
        #ラベル
        layout = QHBoxLayout(self)
        self.label = QLabel(self.labelName, self)
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.label)
        #スピンボックス
        self.__spinBox = QDoubleSpinBox(self)
        self.__spinBox.setMinimumWidth(10)
        self.__spinBox.setMinimumHeight(30)
        self.__spinBox.setSingleStep(0.01)
        self.__spinBox.setAlignment(Qt.AlignRight)
        self.__spinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.__spinBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.__spinBox)
        #スライダー
        self.__slider = QSlider(Qt.Horizontal, self)
        self.__slider.sliderPressed.connect(self.pressed)
        self.__slider.sliderReleased.connect(self.released)
        self.__slider.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addWidget(self.__slider)
        # SliderかSpinBox値が変われば実行し同期させる
        self.__spinBox.valueChanged[float].connect(self.valueChangedCallback)
        self.__slider.valueChanged[int].connect(self.valueChangedCallback)

        #値範囲を指定
        self.setRange(float(self.min), float(self.max))

    #各DCCツールでUndoのチャンク
    def pressed(self):
        #cmds.undoInfo(openChunk=True)
        pass
    def released(self):
        #cmds.undoInfo(closeChunk=True)
        pass

    def valueChangedCallback(self, getValue):
        #イベント発火のWidgetを返す
        sender = self.sender()
        if sender == self.__spinBox:
            self.__slider.blockSignals(True)
            # 少数を打ち消す倍率を適用して、QSliderに値を設定する
            self.__slider.setValue(getValue * self.__boost)
            self.__slider.blockSignals(False)

        elif sender == self.__slider:
            # 少数を打ち消す倍率を適用して、変数の値を上書きする
            # 値を上書きするのは、カスタムのSignalをエミットする必要があるからです。
            getValue = float(getValue)/self.__boost

            self.__spinBox.blockSignals(True)
            self.__spinBox.setValue(getValue)
            self.__spinBox.blockSignals(False)

            self.valueChanged.emit(getValue)

    def getValue(self):
        return self.__spinBox.value()

    def setRange(self, min, max):
        self.__spinBox.setRange(min, max)
        self.__updateSliderRange()  # 範囲が変更されたので、スライダーも更新する

    def __updateSliderRange(self):
        decimals = self.__spinBox.decimals()  # 少数点以下の桁数を取得
        minimum = self.__spinBox.minimum()  # 最小値を取得
        maximum = self.__spinBox.maximum()  # 最大値を取得

        # 少数の桁数を使って、倍率を文字列で求めてintに変換する
        # ＜decimalsが2の場合＞
        # int('1'+('0'*2))は、int('1'+'00')→int('100')となる
        # ＜decimalsが0の場合＞
        # int('1'+('0'*0))は、int('1'+'')→int('1')となる
        #
        self.__boost = int('1'+('0'*decimals))

        # QDoubleSpinBoxの範囲に、少数を打ち消す倍率を掛け算して設定する
        # QDoubleSpinBoxの範囲が「0.00～99.99」の場合、
        # QSliderの範囲は「0～9999」になる
        self.__slider.setRange(minimum*self.__boost, maximum*self.__boost)

    def setValue2(self, val):  # 単純に値を受け取ってSetする。主にUI設定の読込時に使用
        self.__spinBox.setValue(val)

class PyToggle(QCheckBox):
    def __init__(self,width=60,bg_color="#777",circle_color="#DDD",active_color="#00BCff"):
        QCheckBox.__init__(self)
        self.setFixedSize(width,28)
        self.setCursor(Qt.PointingHandCursor)

        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

    #paintEventで設定したRectの範囲をクリックの範囲にする
    #仮想関数
    def hitButton(self,pos:QPoint):   
        return self.contentsRect().contains(pos)
    #仮想関数
    def paintEvent(self,event):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)
        #rect = QRect(0,0,self.width(),self.height())

        #isCheckedで描画分岐
        if not self.isChecked():
            #背景の描画
            qp.setBrush(QColor(self._bg_color))
            qp.drawRoundedRect(0, 0, self.width(), self.height(),
                           self.height()/2, self.height()/2)
            #円の描画
            qp.setBrush(QColor(self._circle_color))
            qp.drawEllipse(3,3,22,22)
        else:
            qp.setBrush(QColor(self._active_color))
            qp.drawRoundedRect(0, 0, self.width(), self.height(),
                               self.height()/2, self.height()/2)
            #円の描画
            qp.setBrush(QColor(self._circle_color))
            qp.drawEllipse(self.width()-26, 3, 22, 22)
        
        qp.end()   

class ImageLabel(QLabel):
    def __init__(self, filename=None, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.setImage(filename)

    def setImage(self, filename):
        self.setPixmap(QPixmap(filename))
        
class DraggableButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(DraggableButton, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        self.__isDrag = True
        self.__startPos = event.pos()
        super(DraggableButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.__isDrag = False
        super(DraggableButton, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.__isDrag:
            self.move(self.mapToParent(event.pos() - self.__startPos))
        super(DraggableButton, self).mouseMoveEvent(event)
        
"""
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = WindowBase()
    window.resize(640, 360)

    layout = QVBoxLayout(window)
    button = DraggableButton('DraggableButton', window)
    button.setFixedSize(128, 32)
    layout.addWidget(button)
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
"""