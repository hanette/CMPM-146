# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow2.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QMovie
import os
from face_detection_morph import match

class Ui_mainwindow2(QWidget):

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        match(fileName)
        if fileName:
            image = QPixmap(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                returnV
            self.label.setPixmap(image)
            self.label_6.setPixmap(image)
    def inputPicture(self):
        self.label_5.setPixmap(self.label_6.pixmap())
    def charPicture(self):
        self.label_5.setPixmap(QtGui.QPixmap("output/char.jpg"))
    def markedChar(self):
        self.label_5.setPixmap(QtGui.QPixmap("output/char_output.jpg"))
    def morph(self):
        self.label_5.setPixmap(QtGui.QPixmap("output/morph.jpg"))
    def markedInput(self):
        self.label_5.setPixmap(QtGui.QPixmap("output/user_output.jpg"))
    def setupUi(self, MainWindow):
        movie = QtGui.QMovie("layout/theloop.gif")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-10, 100, 401, 391))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("layout/Judy Hopps.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(410, 80, 391, 411))
        self.label_2.setMovie(movie)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        movie.start()
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(325, 10, 130, 61))
        self.textEdit.setStyleSheet("background: transparent")
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 520, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 801, 571))
        self.label_3.setStyleSheet("background:white")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("layout/PinClipart.com_disney-character-silhouette-clip_2682263.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 60, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openFileDialog)
        self.pushButton_2.clicked.connect(self.label_3.deleteLater)
        self.pushButton_2.clicked.connect(self.pushButton_2.deleteLater)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(240, 50, 321, 431))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("layout/border.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(290, 10, 271, 74))
        self.textEdit_2.setStyleSheet("background: transparent")
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(260, 70, 281, 391))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("output/char.jpg"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 520, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(500, 520, 113, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(340, 520, 113, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(130, 520, 171, 31))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(620, 520, 171, 21))
        self.pushButton_7.setObjectName("pushButton_7")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(0, 0, 801, 581))
        self.textEdit_3.setReadOnly(True)
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(260, 70, 281, 391))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("output/char.jpg"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_6.raise_()
        self.pushButton_7.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_3.raise_()
        self.textEdit_2.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.textEdit_3.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.textEdit.raise_()
        self.pushButton.raise_()
        self.label_3.raise_()
        self.pushButton_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(self.pushButton.deleteLater)
        self.pushButton.clicked.connect(self.label.deleteLater)
        self.pushButton.clicked.connect(self.label_2.deleteLater)
        self.pushButton.clicked.connect(self.textEdit.deleteLater)
        self.pushButton.clicked.connect(self.textEdit_3.deleteLater)
        self.pushButton_3.clicked.connect(lambda:self.inputPicture())
        self.pushButton_4.clicked.connect(lambda:self.charPicture())
        self.pushButton_5.clicked.connect(lambda:self.morph())
        self.pushButton_6.clicked.connect(lambda:self.markedInput())
        self.pushButton_7.clicked.connect(lambda:self.markedChar())


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:12pt; font-weight:600;\">Analyzing.....</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "See Results"))
        self.pushButton_2.setText(_translate("MainWindow", "Input Picture"))
        self.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:24pt;\">You Look Like:</span></p></body></html>"))
        self.pushButton_3.setText(_translate("MainWindow", "See Input"))
        self.pushButton_4.setText(_translate("MainWindow", "See Match"))
        self.pushButton_5.setText(_translate("MainWindow", "See Morph"))
        self.pushButton_6.setText(_translate("MainWindow", "See Keypoints(Input)"))
        self.pushButton_7.setText(_translate("MainWindow", "See Keypoints(Match)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
