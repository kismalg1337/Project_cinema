from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
import os
import sys
import sqlite3
from for_exql import create_excel, delete_excel


class WhatWeDo(QMainWindow):  # Класс главного меню, выбор нужной функции.
    def __init__(self):
        super(WhatWeDo, self).__init__()
        uic.loadUi('UI_Files\panel_owner.ui', self)
        self.setFixedSize(400, 150)
        self.label.setFont(QtGui.QFont("Arial", 6))
        self.btn_add.clicked.connect(self.add_film)
        self.btn_del.clicked.connect(self.del_film)

    # Открытие меню добавления фильма
    def add_film(self):
        global add
        ex.close()
        add = AddFilm()
        add.show()

    # Открытие меню удаления фильма
    def del_film(self):
        global delete
        ex.close()
        delete = DelFilm()
        delete.show()

    # Вернуться в главное меню
    def back(self):
        ex.close()
        os.system('python Main.py')


class AddFilm(QMainWindow):  # Класс добавления фильмов.
    def __init__(self):
        super(AddFilm, self).__init__()
        uic.loadUi('UI_Files\Add_film.ui', self)
        self.setFixedSize(450, 600)
        self.fname = ''
        self.btn_add_film.clicked.connect(self.add_film)
        self.btn_img.clicked.connect(self.pick_img)

        # Получение названий всех фильмов
        con = sqlite3.connect('Film.db')
        cur = con.cursor()
        for i in cur.execute("""SELECT title from genres""").fetchall():
            self.comboBox.addItem(str(i[0]))
        con.close()

    # Добавление фильма в базу данных и создание xlsx файла с расположением мест
    def add_film(self):
        # Проверка на то, чтобы все поля были заполнены.
        if self.name_film.text() != '' and self.comboBox.currentText() and self.country.text() != '' and \
                self.year.text() != '' and self.duration.text() != '' and \
                self.description.text() != '' and self.fname != '':
            # Получение всех значений из полей + добавление фильма в базу данных.
            con = sqlite3.connect('Film.db')
            cur = con.cursor()
            last_point = cur.execute("""SELECT id FROM Films""").fetchall()
            last_point = [int(str(i)[1:-2]) for i in last_point][-1] + 1
            last_point_opis = cur.execute("""SELECT id FROM Opisanie""").fetchall()
            last_point_opis = [int(str(i)[1:-2]) for i in last_point_opis][-1] + 1
            cur.execute(f'INSERT INTO Opisanie (id, title) VALUES ({last_point_opis}, "{self.description.text()}")')
            con.commit()
            genre = cur.execute(f'SELECT id FROM genres WHERE title = "{self.comboBox.currentText()}"').fetchone()[0]
            cur.execute(f'INSERT INTO Films (id, year, genre, title, duration, Country, photo, description) VALUES \
            ({last_point}, {self.year.text()}, {genre}, "{self.name_film.text()}", \
            {self.duration.text()}, "{self.country.text()}", "{self.fname}", "{last_point_opis}")')
            self.firstdate = [int(i) for i in self.first_date.dateTime().toString('yyyy-MM-dd').split('-')]
            self.lastdate = [int(i) for i in self.last_date.dateTime().toString('yyyy-MM-dd').split('-')]
            create_excel(str(last_point), self.firstdate, self.lastdate)
            con.commit()
            con.close()
            add.close()
            ex.show()
            os.system('python Main.py')

    # Функция получения пути до изображения
    def pick_img(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', 'Картинка (*.jpg)')[0]


class DelFilm(QMainWindow):  # Класс удаления фильмов.
    def __init__(self):
        super(DelFilm, self).__init__()
        uic.loadUi('UI_Files\del_film.ui', self)
        self.setFixedSize(345, 170)
        self.btn_del.clicked.connect(self.del_f)

        # Получение названий всех фильмов
        con = sqlite3.connect('Film.db')
        cur = con.cursor()
        for i in cur.execute("""SELECT title from Films""").fetchall():
            self.comboBox.addItem(str(i[0]))

    # Удаление фильма из базы данных + удаление файла xlsx
    def del_f(self):
        con = sqlite3.connect('Film.db')
        cur = con.cursor()
        idl = int(cur.execute(f'SELECT id FROM Films WHERE title = "{self.comboBox.currentText()}"').fetchone()[0])
        idl_2 = int(
            cur.execute(f'SELECT description FROM Films WHERE title = "{self.comboBox.currentText()}"').fetchone()[0])
        cur.execute(f'DELETE FROM Films WHERE title = "{self.comboBox.currentText()}"')
        cur.execute(f'DELETE FROM Opisanie WHERE id = {idl_2}')
        delete_excel(f'sits\{idl}.xlsx')
        con.commit()
        con.close()
        delete.close()
        ex.show()
        os.system('python Main.py')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WhatWeDo()
    ex.show()
    sys.exit(app.exec())
