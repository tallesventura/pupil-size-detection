from PyQt4 import QtGui, QtCore
from progressBar import Ui_loadingUi
import time
from videoProcessor import VideoProcessor
import os

class PDLoading (QtGui.QWidget):

    def __init__(self, path_video, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_loadingUi()
        self.ui.setupUi(self)
        self.value = 1
        self.path_video = path_video
        self.dest_path = os.path.basename(self.path_video)
        self.video_task = VideoProcessor(path_video)
        self.ui.progressBar.setValue(self.value)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(204)
        self.ui.cancel_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self._active = True
        self.video_task.start()
        self.video_processing()
        self.video_task.notifyProgress.connect(self.on_progress)
        # self.exec_loading()


    # def exec_loading(self):
    #     if self._active:
    #         if self.ui.progressBar.value() == self.ui.progressBar.maximum():
    #             self.ui.progressBar.reset()
    #         QtCore.QTimer.singleShot(0, self.video_processing)
    #     else:
    #         self._active = False

    def closeEvent(self):
        self.destroy(True)

    def on_progress(self, i):
        self.ui.progressBar.setValue(i)

    def video_processing(self):
        while True:
            time.sleep(0.05)
            if self.value == 204:
                break
            else:
                self.video_task.run(self.dest_folder, self.path_video, 1)

        self.destroy(True)






