from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import sys


class AboutUs(QMainWindow):  # Класс описания кинотеатра
    def __init__(self):
        super(AboutUs, self).__init__()
        uic.loadUi('UI_Files\About us.ui', self)
        self.auto_pull()

    def auto_pull(self):
        self.setStyleSheet('.QWidget {background-color: #d9d4fb;}')
        self.setFixedSize(550, 640)
        self.label_main.setText('Кинотетр "Космос"')
        self.label_main.setFont(QtGui.QFont('Arial Black', 18))

        self.label_photo.setStyleSheet('.QLabel {background-image: url(images/Cinema_view.png);}')

        self.label_description.setText('Кинотеатр «Космос» предоставляет возможность погрузиться в разнообразный '
                                       'мир кино и профессионально, учитывая современные тенденции, '
                                       'обеспечит для вас процесс получения новых переживаний.Кинотеатр «Космос» '
                                       'был построен в 1967 г. К современному виду «Космос» пришел не сразу. '
                                       'В 2003 году началась реконструкция основного старого здания кинотеатра. '
                                       'Архитектура здания была сильно изменена, сменился интерьер, установлено '
                                       'широкоформатное оборудование. Первоначально в зрительском зале было 810 '
                                       'жестких фанерных мест. После реконструкции пристроено фойе — 1000 квадратных '
                                       'метров, в том числе гардероб на 650 мест, зрительный зал на 476 удобных '
                                       'кресел. Была полностью заменена система энергоснабжения, акустика. Система '
                                       'кондиционирования и вентиляции. Сегодня в кинотеатре установлена система '
                                       'Dolby DTS, цифровое (3D) кинопроекционное оборудование. В 2015 году был '
                                       'установлен новый, современный Серебряный экран Harkness Spectral 240 3D '
                                       'silver screens. В 2005 г. было построено новое здание кинотеатра. '
                                       'Особенность здания заключается в том, что большая часть расположена '
                                       'под землей. В новом здании кинотеатра размещается пять зрительных залов, '
                                       'билетные кассы, ресторан и рестобар. Каждый из 5 залов рассчитан на 138 мест. '
                                       'Мы ждем Вас всегда. Приходите и мы подарим вам '
                                       'ощущение бесконечного праздника!')
        self.label_description.setFont(QtGui.QFont('Georgia', 8))

        self.btn_back.clicked.connect(self.back)
        self.btn_back.setFont(QtGui.QFont('Georgia', 8))

    # Вернуться в главное меню
    def back(self):
        ex.close()
        os.system('python Main.py')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AboutUs()
    ex.show()
    sys.exit(app.exec())
