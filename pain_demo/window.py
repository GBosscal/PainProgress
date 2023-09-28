# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,pyqtSignal
class Ui_MainWindow(object):
    # 定义一个信号，pyqtSignal用于创建自定义信号
    signal = pyqtSignal()
    # 设置界面布局和元素
    def setupUi(self, MainWindow):
        # 设置窗口的名称和大小
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(562, 372)
        # 创建一个QWidget作为主要部分
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        # 创建两个按钮
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        #self.pushButton.setGeometry(QtCore.QRect(80, 20, 93, 28))
        self.pushButton.setGeometry(QtCore.QRect(300, 20, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        #self.pushButton_2.setGeometry(QtCore.QRect(370, 20, 93, 28))
        self.pushButton_2.setGeometry(QtCore.QRect(1050, 20, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        # 创建两个图形显示区域
        self.graphicsView = QtWidgets.QGraphicsView(self.centralWidget)
        #self.graphicsView.setGeometry(QtCore.QRect(50, 60, 191, 231))
        self.graphicsView.setGeometry(QtCore.QRect(50, 60, 191*3, 231*3))
        #（左上角的x和y,矩形的高度和宽度）
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralWidget)
        #self.graphicsView_2.setGeometry(QtCore.QRect(330*2, 60, 191*3, 231*3))
        self.graphicsView_2.setGeometry(QtCore.QRect(400*2, 60, 191*3, 231*3))
        self.graphicsView_2.setObjectName("graphicsView_2")
        # 创建一个下拉选项框
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        #self.comboBox.setGeometry(QtCore.QRect(230, 20, 111, 31))
        self.comboBox.setGeometry(QtCore.QRect(650, 20, 111, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")# 向下拉选项框添加一个选项
        # 将centralWidget设置为窗口的主要部分
        MainWindow.setCentralWidget(self.centralWidget)
        # 创建菜单栏、工具栏和状态栏
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 562, 26))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        # 设置窗口图标
        self.setWindowIcon(QIcon('icons/icon.png'))
        # 设置界面元素的文本内容
        self.retranslateUi(MainWindow)
         # 连接界面元素的信号和槽
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
 # 设置界面元素的本地化文本
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "疼痛识别系统"))
        self.pushButton.setText(_translate("MainWindow", "导入"))
        self.pushButton_2.setText(_translate("MainWindow", "保存"))
        self.comboBox.setItemText(0, _translate("MainWindow", "识别"))

