# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PDMainWindow.ui'
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

class Ui_PDMainWindow(object):
    def setupUi(self, PDMainWindow):
        PDMainWindow.setObjectName(_fromUtf8("PDMainWindow"))
        PDMainWindow.resize(796, 610)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/eye-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PDMainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(PDMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(190, 10, 441, 551))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.eye_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.eye_label.setText(_fromUtf8(""))
        self.eye_label.setPixmap(QtGui.QPixmap(_fromUtf8("resources/Eye Scapes - 01b.png")))
        self.eye_label.setObjectName(_fromUtf8("eye_label"))
        self.verticalLayout.addWidget(self.eye_label)
        self.welcome_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.welcome_label.setTextFormat(QtCore.Qt.AutoText)
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome_label.setObjectName(_fromUtf8("welcome_label"))
        self.verticalLayout.addWidget(self.welcome_label)
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.upload_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.upload_button.setObjectName(_fromUtf8("upload_button"))
        self.horizontalLayout.addWidget(self.upload_button)
        self.open_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.open_button.setObjectName(_fromUtf8("open_button"))
        self.horizontalLayout.addWidget(self.open_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        PDMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(PDMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PDMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PDMainWindow)
        QtCore.QMetaObject.connectSlotsByName(PDMainWindow)

    def retranslateUi(self, PDMainWindow):
        PDMainWindow.setWindowTitle(_translate("PDMainWindow", "Pupil Size Detection", None))
        self.welcome_label.setText(_translate("PDMainWindow", "Welcome to Automatic Pupil Size Detection!", None))
        self.label.setText(_translate("PDMainWindow", "Click the button to Upload a video or Open to previous project", None))
        self.upload_button.setText(_translate("PDMainWindow", "Upload", None))
        self.open_button.setText(_translate("PDMainWindow", "Open Project", None))

