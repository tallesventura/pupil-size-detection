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
        loadingUi.resize(273, 102)
        self.formLayoutWidget = QtGui.QWidget(loadingUi)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 10, 271, 91))
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
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.label_3)

        self.retranslateUi(loadingUi)
        QtCore.QMetaObject.connectSlotsByName(loadingUi)

    def retranslateUi(self, loadingUi):
        loadingUi.setWindowTitle(_translate("loadingUi", "Form", None))
        self.process_label.setText(_translate("loadingUi", "Processing video", None))
        self.label_3.setText(_translate("loadingUi", "Loading...   ", None))

