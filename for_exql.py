import openpyxl
from datetime import date, timedelta
import os


# Функция создания xlsx файлов, в которых хранится информация о том какие места заняты, а какие нет.
def create_excel(name, f1, s1):
    filepath = f'D:\PyCharm 2019.2.3\Project\First year\Second year\Cinema_project\sits\{name}.xlsx'
    wb = openpyxl.Workbook()
    sheet = wb.active
    # Основная информация для заполнения.
    ak = "row_1_btn_1,row_1_btn_2,row_1_btn_3,row_1_btn_4,row_1_btn_5,row_1_btn_6,row_1_btn_7," \
         "row_1_btn_8,row_1_btn_9,row_1_btn_10,row_1_btn_11,row_1_btn_12,row_2_btn_1," \
         "row_2_btn_2,row_2_btn_3,row_2_btn_4,row_2_btn_5,row_2_btn_6,row_2_btn_7,row_2_btn_8," \
         "row_2_btn_9,row_2_btn_10,row_2_btn_11,row_2_btn_12,row_2_btn_13,row_2_btn_14,row_3_btn_1," \
         "row_3_btn_2,row_3_btn_3,row_3_btn_4,row_3_btn_5,row_3_btn_6,row_3_btn_7,row_3_btn_8,row_3_btn_9," \
         "row_3_btn_10,row_3_btn_11,row_3_btn_12,row_3_btn_13,row_3_btn_14,row_4_btn_1,row_4_btn_2,row_4_btn_3," \
         "row_4_btn_4,row_4_btn_5,row_4_btn_6,row_4_btn_7,row_4_btn_8,row_4_btn_9,row_4_btn_10," \
         "row_4_btn_11,row_4_btn_12,row_4_btn_13,row_4_btn_14,row_4_btn_15,row_4_btn_16,row_5_btn_1," \
         "row_5_btn_2,row_5_btn_3,row_5_btn_4,row_5_btn_5,row_5_btn_6,row_5_btn_7,row_5_btn_8,row_5_btn_9," \
         "row_5_btn_10,row_5_btn_11,row_5_btn_12,row_5_btn_13,row_5_btn_14,row_5_btn_15,row_5_btn_16,row_6_btn_1," \
         "row_6_btn_2,row_6_btn_3,row_6_btn_4,row_6_btn_5,row_6_btn_6,row_6_btn_7,row_6_btn_8,row_6_btn_9," \
         "row_6_btn_10,row_6_btn_11,row_6_btn_12,row_6_btn_13,row_6_btn_14,row_6_btn_15,row_6_btn_16," \
         "row_6_btn_17,row_6_btn_18,row_7_btn_1,row_7_btn_2,row_7_btn_3,row_7_btn_4,row_7_btn_5,row_7_btn_6," \
         "row_7_btn_7,row_7_btn_8,row_7_btn_9,row_7_btn_10,row_7_btn_11,row_7_btn_12,row_7_btn_13,row_7_btn_14," \
         "row_7_btn_15,row_7_btn_16,row_7_btn_17,row_7_btn_18,row_8_btn_1,row_8_btn_2,row_8_btn_3," \
         "row_8_btn_4,row_8_btn_5,row_8_btn_6,row_8_btn_7,row_8_btn_8,row_8_btn_9,row_8_btn_10," \
         "row_8_btn_11,row_8_btn_12,row_8_btn_13,row_8_btn_14,row_8_btn_15,row_8_btn_16,row_8_btn_17," \
         "row_8_btn_18,row_8_btn_19,row_8_btn_20,row_9_btn_1,row_9_btn_2,row_9_btn_3,row_9_btn_4," \
         "row_9_btn_5,row_9_btn_6,row_9_btn_7,row_9_btn_8,row_9_btn_9,row_9_btn_10,row_9_btn_11," \
         "row_9_btn_12,row_9_btn_13,row_9_btn_14,row_9_btn_15,row_9_btn_16,row_9_btn_17,row_9_btn_18," \
         "row_9_btn_19,row_9_btn_20"
    sheet['A1'].value = 'film'
    sheet['B1'].value = 'time'
    sheet['C1'].value = 'sits'
    sheet['D1'].value = 'day'

    # Получение времени, в течении которго фильм будет в прокате.
    d1 = date(f1[0], f1[1], f1[2])  # начальная дата
    d2 = date(s1[0], s1[1], s1[2])  # конечная дата
    all_days = 0
    delta = d2 - d1  # timedelta
    days = list()
    for i in range(delta.days + 1):
        ap = str(d1 + timedelta(i)).split('-')
        days.append('.'.join([ap[2], ap[1], ap[0]]))

    # Заполнение xlsx файла данными.
    for i in range(len(days)):
        for j in range(0, 4):
            if j == 0:
                sheet[f'B{2 + j + i * 4}'].value = "11:00:00"
            if j == 1:
                sheet[f'B{2 + j + i * 4}'].value = "15:00:00"
            if j == 2:
                sheet[f'B{2 + j + i * 4}'].value = "19:00:00"
            if j == 3:
                sheet[f'B{2 + j + i * 4}'].value = "21:00:00"
            all_days += 1
            sheet[f'C{2 + j + i * 4}'].value = ak
            sheet[f'D{2 + j + i * 4}'].value = f'"{days[i]}"'
    sheet[f'J1'].value = all_days

    wb.save(filepath)


# Функия удаления файла xlsx
def delete_excel(name):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(name))
    os.remove(path)
