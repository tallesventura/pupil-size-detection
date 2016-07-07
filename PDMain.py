#!/usr/env python

import os, sys
from PyQt4 import QtCore, QtGui
from PDMainWindow import Ui_PDMainWindow
from PDLoading import PDLoading



class PDMain(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_PDMainWindow()
        self.ui.setupUi(self)
        self.ui.upload_button.clicked.connect(self.get_path_file)
        self.ui.open_button.clicked.connect(self.get_path_folder)
        self.loading_ui = None

    def get_path_file(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        if os.path.isfile(self.filename):
            self.show_progressBar(self.filename)

    def get_path_folder(self):
        fd = QtGui.QFileDialog(self)
        self.path = fd.getExistingDirectory()
        print(self.path)

    def show_progressBar(self, path_video):
         if self.loading_ui is None:
             self.loading_ui = PDLoading(path_video)
         self.loading_ui.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = PDMain()
    myapp.show()
    sys.exit(app.exec_())