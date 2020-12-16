import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sqlite3
import openpyxl
import os
from PyQt5.QtCore import Qt


class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        uic.loadUi('UI_Files\MainWindow.ui', self)

        # Заполнение верхней панели переключения.
        self.setStyleSheet('.QWidget {background-image: url(images/new.jpg);}')
        # self.setStyleSheet('.QWidget {background-color: #064199}')
        self.groupBox_2.setStyleSheet('.QGroupBox {background-color: #000000}')
        self.label.setStyleSheet('.QLabel {background-image: url(images/Screenshot_3.png);}')
        self.btn_1.setStyleSheet('.QPushButton {color: #8A2BE2; background-color: #000000;} '
                                 '.QPushButton:pressed {color: #9400D3; text-decoration: underline}')
        self.btn_1.setFont(QtGui.QFont('CeraPro-Bold', 18))
        self.btn_1.clicked.connect(self.rasp)
        self.btn_2.setStyleSheet('.QPushButton {color: #8A2BE2; background-color: #000000;} '
                                 '.QPushButton:pressed {color: #9400D3; text-decoration: underline}')
        self.btn_2.setFont(QtGui.QFont('CeraPro-Bold', 18))
        self.btn_2.clicked.connect(self.rasp)
        self.btn_3.setStyleSheet('.QPushButton {color: #8A2BE2; background-color: #000000;} '
                                 '.QPushButton:pressed {color: #9400D3; text-decoration: underline}')
        self.btn_3.setFont(QtGui.QFont('CeraPro-Bold', 18))
        self.btn_3.clicked.connect(self.about)
        self.btn_4.setStyleSheet('.QPushButton {color: #8A2BE2; background-color: #000000;} '
                                 '.QPushButton:pressed {color: #9400D3; text-decoration: underline}')
        self.btn_4.setFont(QtGui.QFont('CeraPro-Bold', 18))
        self.btn_4.clicked.connect(self.rasp)
        self.setFixedSize(900, 700)
        self.count = 0
        self.main_films()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
            if event.key() == Qt.Key_C:
                ex.close()
                os.system('python panel_owner.py')

    def main_films(self):
        con = sqlite3.connect('Film.db')
        cur = con.cursor()
        self.result = cur.execute("""SELECT id FROM Films""").fetchall()
        self.result = [str(i)[1:-2] for i in self.result]
        self.ids = list()
        # Добавить очищение в функции переключения фильмов
        # Заполнение картинками главного экрана.
        for i in enumerate(self.result):
            if i[0] < 8:
                idm = cur.execute(f'SELECT photo FROM Films WHERE id = {i[1]}').fetchone()[0]
                eval(f"self.label_{int(i[0]) + 1}.setStyleSheet('.QLabel " +
                     "{background-image: url(" + f'{idm}' + ");}')")
                self.ids.append(idm)
            else:
                break
        con.close()

        # Подключение каждого филдьма к своей кнопке.
        for i in range(1, 9):
            eval(f'self.pushButton_{i}.clicked.connect(self.more)')
            eval(f"self.pushButton_{i}.setStyleSheet('.QPushButton" + "{color: #8A2BE2; background-color: #D3D3D3;}')")
        self.btn_next.setStyleSheet('.QPushButton {background-image: url(images/35.png);}')  # Кнопка переключения фильмов
        self.btn_next.clicked.connect(self.next)

    def more(self):
        global more, id_ct_2, id_ct_photo
        con = sqlite3.connect('Film.db')
        cur = con.cursor()
        id_ct_2 = int(self.sender().objectName().split('_')[-1]) + self.count
        id_ct_photo = cur.execute(f'SELECT photo from Films where id = "{id_ct_2}"').fetchone()[0]
        con.close()
        ex.hide()
        more = NewMore()
        more.show()

    def about(self):
        ex.close()
        os.system('python about_us.py')

    def rasp(self):
        global pas
        pas = BronPass()
        ex.hide()
        pas.show()

    def next(self):
        # Функция прокрутки фильмов для дальнейшего просмотра
        self.count += 1
        dl = len(self.result) - 8
        con = sqlite3.connect('Film.db')
        cur = con.cursor()
        if self.count <= dl:
            self.ids = list()
            for i in range(len(self.result)):
                if 0 + self.count <= i < 8 + self.count:
                    idm = cur.execute(f'SELECT photo FROM Films WHERE id = {self.result[i]}').fetchone()[0]
                    eval(f"self.label_{i + 1 - self.count}.setStyleSheet('.QLabel " +
                         "{background-image: url(" + f'{idm}' + ");}')")
                    eval(f'self.label_{i + 1 - self.count}.repaint()')
                    self.ids.append(idm)
        else:
            self.ids = list()
            self.count = 0
            for i in enumerate(self.result):
                if 0 <= i[0] < 8:
                    idm = cur.execute(f'SELECT photo FROM Films WHERE id = {i[1]}').fetchone()[0]
                    eval(f"self.label_{int(i[0]) + 1}.setStyleSheet('.QLabel " +
                         "{background-image: url(" + f'{idm}' + ");}')")
                    self.ids.append(idm)
        con.close()


class NewMore(QMainWindow):  # Описание фильма + выбор времени сеанса.
    def __init__(self):
        super(NewMore, self).__init__()
        uic.loadUi('UI_Files\more.ui', self)
        self.data = ''
        self.time = ''
        self.auto_pull()

    def auto_pull(self):  # Получение всей информации из SQL.
        global info_about_film
        con = sqlite3.connect('Film.db')
        cur = con.cursor()
        self.setFixedSize(700, 735)
        self.setStyleSheet('.QWidget {background-color: #d9d4fb;}')
        self.label_1.setStyleSheet('.QLabel {background-image: url(' + str(id_ct_photo) + ');}')
        id_m = cur.execute("""SELECT * from Films Where id =""" + str(id_ct_2)).fetchmany(12)
        genre = cur.execute("""SELECT title from genres where id = (SELECT genre from Films where 
        id =""" + str(id_ct_2) + """)""").fetchall()
        description = cur.execute("""SELECT title from opisanie where id = (SELECT description from Films where 
        id =""" + str(id_ct_2) + """)""").fetchall()
        con.close()
        self.label_description.setFont(QtGui.QFont('Georgia', 12))
        self.label_description.setText(f'Фильм: {id_m[0][4]}\n-------------------------------\n'
                                       f'Жанр: {str(genre[0][0])}\n-------------------------------\n'
                                       f'Год выпуска: {id_m[0][1]}\n-------------------------------\n'
                                       f'Страна производителя: {id_m[0][5]}\n-------------------------------\n'
                                       f'Продолжительность: {id_m[0][3]}\n-------------------------------\n'
                                       f'Описание: {str(description[0][0])}')
        info_about_film = self.label_description.text()
        self.label_text.setFont(QtGui.QFont("Courier New", 16))
        self.label_text.setStyleSheet('.QLabel {color: #ff00ff;}')
        self.btn_back.clicked.connect(self.back)
        self.btn_back.setFont(QtGui.QFont('Georgia', 8))
        self.buy_tick.clicked.connect(self.buy)
        self.calendarWidget.clicked.connect(self.date)
        self.calendarWidget.setGridVisible(True)

        self.btn_11.clicked.connect(self.timing)
        self.btn_15.clicked.connect(self.timing)
        self.btn_19.clicked.connect(self.timing)
        self.btn_21.clicked.connect(self.timing)

    # Функция определения даты сеанса.
    def date(self):
        a = self.calendarWidget.selectedDate().toString().split(' ')
        self.data = ' '.join([a[2], a[1], a[3]])
        self.check()

    # Функция определения времени сеанса.
    def timing(self):
        self.time = self.sender().text()
        self.check()

    # Функция проверки на наличие двух параметров(время и дата)
    def check(self):
        if self.time != '' and self.data != '':
            self.info_buy.setText(f'Ваше время; {self.data} {self.time}')

    # Выход в главное меню.
    def back(self):
        more.close()
        os.system('python Main.py')

    # Переход на следующий этап покупки.
    def buy(self):
        global boyed
        more.close()
        boyed = BuyTickets()
        boyed.show()


class BronPass(QMainWindow):
    def __init__(self):
        super(BronPass, self).__init__()
        uic.loadUi('UI_Files\Bron_pass.ui', self)
        self.pushButton.clicked.connect(self.ppp)

    def ppp(self):
        pas.hide()
        ex.show()


class BuyTickets(QMainWindow):  # Покупка билетов.
    def __init__(self):
        super(BuyTickets, self).__init__()
        uic.loadUi('UI_Files\Buy_tickets.ui', self)
        self.buy = []
        self.sits = []
        self.count = int()

        self.auto_pull()

    def auto_pull(self):
        # Заполнение верхнего фона, декорации.
        con = sqlite3.connect('Film.db')
        cur = con.cursor()
        con.close()
        self.setStyleSheet('.QWidget {background-color: #696969}')

        self.info.setText(
            '-------------------------------'.join(str(info_about_film).split('-------------------------------')[0:5]))
        self.info.setFont(QtGui.QFont('Georgia', 9))
        self.info.setStyleSheet('.QLabel {color: #FFFFFF}')

        self.info_2.setText(f'Зал номер: \n-------------\n'
                            f'Время сеанса: \n-------------\n')
        self.info_2.setFont(QtGui.QFont('Georgia', 9))
        self.info_2.setStyleSheet('.QLabel {color: #FFFFFF}')

        self.screen.setStyleSheet('.QLabel {background-image: url(images/Screenshot_27.png);}')

        self.main_sit.setStyleSheet(".QPushButton {border-radius: 12px; background-color: #0000FF;}")
        self.main_sit.setText('')
        self.legend_sit.setStyleSheet(".QPushButton {border-radius: 12px; background-color: #00FF00;}")
        self.legend_sit.setText('')
        self.bought_sit.setStyleSheet(".QPushButton {border-radius: 12px; background-color: #808080;}")
        self.bought_sit.setText('')

        # Определение времени выбранного сеанса.
        dates = {'янв': '01', 'фев': '02', 'мар': '03', 'апр': '04',
                 'май': '05', 'июн': '06', 'июл': '07', 'авг': '08',
                 'сен': '09', 'окт': '10', 'ноя': '11', 'дек': '12'}
        timing = more.info_buy.text().split(';')[1].strip().split(' ')
        timing[3], timing[1] = timing[3] + ':00', dates[timing[1]]
        data = '.'.join(timing[0:3])
        time = timing[3]
        wb = openpyxl.load_workbook(
            filename=f'sits\{str(id_ct_2)}.xlsx')
        sheet = wb.active
        count = int(sheet['J1'].value)

        # Определение номера строки в Exсel таблице.
        self.beta = int()
        for i in range(2, count + 2):
            if eval(f"str(sheet['D{i}'].value[1:-1]) == data and str(sheet['B{i}'].value) == time"):
                self.beta = i
                break

        # Кнопка покупки билетов.
        self.btn_buy.clicked.connect(self.bought)

        # Окрашивание кнопок цветами, по признаку покупки.
        for i in range(1, 10):
            if i == 1:
                for j in range(1, 13):
                    if eval(
                            f"str(self.row_{str(i)}_btn_{str(j)}.objectName()) in sheet['C{str(self.beta)}'].value.split(',')"):
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #00FF00; color: #800000}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.clicked.connect(self.select_sit)')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setText(str({j}))')

                    else:
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #808080; color: #800000}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}' + ".setText('')")
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setEnabled(False)')
            elif i == 2 or i == 3:
                for j in range(1, 15):
                    if eval(
                            f"str(self.row_{str(i)}_btn_{str(j)}.objectName()) in sheet['C{str(self.beta)}'].value."
                            f"split(',')"):
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #0000FF; color: #FFFFFF}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setText(str({j}))')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.clicked.connect(self.select_sit)')
                    else:
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #808080; color: #800000}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}' + ".setText('')")
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setEnabled(False)')
            elif i == 4 or i == 5:
                for j in range(1, 17):
                    if eval(
                            f"str(self.row_{str(i)}_btn_{str(j)}.objectName()) in sheet['C{str(self.beta)}'].value."
                            f"split(',')"):
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #0000FF; color: #FFFFFF}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setText(str({j}))')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.clicked.connect(self.select_sit)')
                    else:
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #808080; color: #800000}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}' + ".setText('')")
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setEnabled(False)')
            elif i == 6 or i == 7:
                for j in range(1, 19):
                    if eval(
                            f"str(self.row_{str(i)}_btn_{str(j)}.objectName()) in sheet['C{str(self.beta)}'].value."
                            f"split(',')"):
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #0000FF; color: #FFFFFF}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setText(str({j}))')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.clicked.connect(self.select_sit)')
                    else:
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #808080; color: #800000}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}' + ".setText('')")
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setEnabled(False)')
            elif i == 8 or i == 9:
                for j in range(1, 21):
                    if eval(
                            f"str(self.row_{str(i)}_btn_{str(j)}.objectName()) in sheet['C{str(self.beta)}'].value."
                            f"split(',')"):
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #00FF00; color: #800000}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setText(str({j}))')
                        eval(f'self.row_{str(i)}_btn_{str(j)}.clicked.connect(self.select_sit)')
                    else:
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setStyleSheet\
                        (".QPushButton ' + '{border-radius: 12px; background-color: #808080; color: #800000}")')
                        eval(f'self.row_{str(i)}_btn_{str(j)}' + ".setText('')")
                        eval(f'self.row_{str(i)}_btn_{str(j)}.setEnabled(False)')
        for i in range(1, 19):
            eval(f'self.label_{str(i)}.setStyleSheet(".QLabel ' + '{color: #FFFFFF}")')

    # Функция, которая добавляет все выбранные места в список покупок.
    def select_sit(self):
        self.sender().setStyleSheet(".QPushButton {border-radius: 12px; background-color: #ff0000; color: white}")
        row = int(str(self.sender().objectName()).split('_')[1])
        if row == 1 or row == 8 or row == 9:
            self.buy.append((self.sender().objectName(), 400))
        else:
            self.buy.append((self.sender().objectName(), 220))  # При повторном выборе мест покупается сразу по 2. Нужно Решить
        self.sender().setEnabled(False)
        self.count += 1
        summa = sum([i[1] for i in self.buy])
        self.whatbuy.setText(f'Вы выбрали: {self.count} мест. На сумму: {summa}')

    # Функция, самой покупки(удаление из Excel)
    def bought(self):
        wb = openpyxl.load_workbook(
            filename=f'sits\{str(id_ct_2)}.xlsx')
        sheet = wb.active
        new = sheet[f'C{str(self.beta)}'].value.split(',')
        for i in self.buy:
            new.remove(i[0])
        sheet[f'C{str(self.beta)}'].value = ','.join(new)
        wb.save(f'sits\{str(id_ct_2)}.xlsx')
        self.count = 0
        self.buy = list()
        self.whatbuy.setText('Выберите места.')
        self.auto_pull()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())
