import sys
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGroupBox
from PIL import Image
from PIL.ImageQt import ImageQt
import sqlite3
import Main


class Bron_pass(QMainWindow):
    def __init__(self):
        super(Bron_pass, self).__init__()
        uic.loadUi('UI_Files\Bron_pass.ui', self)
        self.pushButton.cliced.connect(self.ppp)

    def ppp(self):
        qpp = Main.MyPillow()
        qpp.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Bron_pass()
    ex.show()
    sys.exit(app.exec())
