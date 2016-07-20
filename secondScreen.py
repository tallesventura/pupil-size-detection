# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'secondScreen.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName(_fromUtf8("Widget"))
        Widget.resize(1439, 745)
        self.listView = QtGui.QListView(Widget)
        self.listView.setGeometry(QtCore.QRect(1200, 0, 241, 621))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.scrollArea = QtGui.QScrollArea(Widget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 1201, 621))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1199, 619))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalScrollBar = QtGui.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar.setGeometry(QtCore.QRect(1220, 0, 20, 621))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName(_fromUtf8("verticalScrollBar"))
        self.verticalScrollBar_3 = QtGui.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar_3.setGeometry(QtCore.QRect(1180, 0, 20, 621))
        self.verticalScrollBar_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_3.setObjectName(_fromUtf8("verticalScrollBar_3"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalScrollBar_2 = QtGui.QScrollBar(Widget)
        self.verticalScrollBar_2.setGeometry(QtCore.QRect(1420, 0, 20, 621))
        self.verticalScrollBar_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_2.setObjectName(_fromUtf8("verticalScrollBar_2"))
        self.pushButton = QtGui.QPushButton(Widget)
        self.pushButton.setGeometry(QtCore.QRect(1200, 650, 101, 61))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Widget)
        self.pushButton_2.setGeometry(QtCore.QRect(1320, 650, 101, 61))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Widget)
        self.pushButton_3.setGeometry(QtCore.QRect(352, 670, 91, 41))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(Widget)
        self.pushButton_4.setGeometry(QtCore.QRect(530, 670, 91, 41))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(_translate("Widget", "Widget", None))
        self.pushButton.setText(_translate("Widget", "Edit image", None))
        self.pushButton_2.setText(_translate("Widget", "Delete image", None))
        self.pushButton_3.setText(_translate("Widget", "Run detection", None))
        self.pushButton_4.setText(_translate("Widget", "Save", None))

