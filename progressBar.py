# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressBar.ui'
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

class Ui_loadingUi(object):
    def setupUi(self, loadingUi):
        loadingUi.setObjectName(_fromUtf8("loadingUi"))
        loadingUi.resize(303, 107)
        self.formLayoutWidget = QtGui.QWidget(loadingUi)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 10, 301, 51))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.process_label = QtGui.QLabel(self.formLayoutWidget)
        self.process_label.setObjectName(_fromUtf8("process_label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.process_label)
        self.progressBar = QtGui.QProgressBar(self.formLayoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.progressBar)
        self.verticalLayoutWidget = QtGui.QWidget(loadingUi)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 70, 131, 31))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cancel_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.verticalLayout.addWidget(self.cancel_button)

        self.retranslateUi(loadingUi)
        QtCore.QMetaObject.connectSlotsByName(loadingUi)

    def retranslateUi(self, loadingUi):
        loadingUi.setWindowTitle(_translate("loadingUi", "Form", None))
        self.process_label.setText(_translate("loadingUi", "Processing video...", None))
        self.cancel_button.setText(_translate("loadingUi", "Cancel", None))

