from PyQt4 import QtGui, QtCore
from progressBar import Ui_loadingUi
import time

class PDLoading (QtGui.QWidget):

    def __init__(self, path_video, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_loadingUi()
        self.ui.setupUi(self)
        self.ui.progressBar.setMinimum(1)
        self.ui.progressBar.setMaximum(100)
        self.ui.cancel_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self._active = True
        self.exec_loading()

    def exec_loading(self):
        if self._active:
            if self.ui.progressBar.value() == self.ui.progressBar.maximum():
                self.ui.progressBar.reset()
            QtCore.QTimer.singleShot(0, self.video_processing)
        else:
            self._active = False

    def closeEvent(self, event):
        self._active = False

    def video_processing(self):
        while True:
            time.sleep(0.05)
            value = self.ui.progressBar.value() + 1
            self.ui.progressBar.setValue(value)







