#!/usr/env python

import os, sys
from PyQt4 import QtCore, QtGui
from PDMainWindow import Ui_PDMainWindow


class PDMain(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_PDMainWindow()
        self.ui.setupUi(self)
        self.ui.upload_button.clicked.connect(self.get_path_file)
        self.ui.open_button.clicked.connect(self.get_path_folder)
        self.window2 = None

    def get_path_file(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        if os.path.isfile(self.filename):
            print(self.filename)

    def get_path_folder(self):
        fd = QtGui.QFileDialog(self)
        self.path = fd.getExistingDirectory()
        print(self.path)

    # def show_window2(self):
    #     if self.window2 is None:
    #         self.window2 = Windows(self)
    #     self.window2.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = PDMain()
    myapp.show()
    sys.exit(app.exec_())