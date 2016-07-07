from PyQt4 import QtGui, QtCore
from progressBar import Ui_loadingUi


class PDLoading (QtGui.QWidget):

    def __init__(self, path_video, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_loadingUi()
        self.ui.setupUi(self)
        self.percent = 0
        self.ui.progressBar.setValue(self.percent)
        while self.percent < 100:
            self.percent += 0.001
            self.ui.progressBar.setValue(self.percent)



