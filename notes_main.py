from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel, QVBoxLayout, QTextEdit, QLineEdit, QListWidget, QHBoxLayout, QInputDialog
import json

def show_note():
    key = list_widget1.selectedItems()[0].text()
    text_edit.setText(notes[key]['текст'])
    list_widget2.clear()   
    list_widget2.addItems(notes[key]['теги'])

def add_note():
    notes_name, ok = QInputDialog.getText(window, 'Добавить заметку','Название заметки:')
    if ok:
        notes[notes_name] = {
            'текст': '',
            'теги': []
        }
    list_widget1.clear()
    list_widget1.addItems(notes)
    with open ('notes_data.json', 'w') as file:
        json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def del_note():
    if list_widget1.selectedItems():
        key = list_widget1.selectedItems()[0].text()
        del notes[key]
        list_widget1.clear()
        list_widget1.addItems(notes)
        text_edit.clear()
        list_widget2.clear()
        with open('notes_data.json',"w") as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def save_note():
    if list_widget1.selectedItems():
        key = list_widget1.selectedItems()[0].text()
        notes[key]['текст'] = text_edit.toPlainText()
        with open('notes_data.json',"w") as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def add_tag():
    if list_widget1.selectedItems():
        key = list_widget1.selectedItems()[0].text()
        tag = line_edit.text()
        if tag != "" and not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_widget2.clear()
            line_edit.clear()
            with open('notes_data.json',"w") as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False)


def del_tag():
    if list_widget2.selectedItems():
        key = list_widget1.selectedItems()[0].text()
        tag = list_widget2.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_widget2.clear()
        list_widget2.addItems(notes[key]['теги'])
        with open('notes_data.json',"w") as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def search_tag():
    tag = line_edit.text()
    if tag != "" and button6.text() == 'Искать заметки по тегу':
        notes_filtered = dict()
        for key in notes:
            if tag in notes[key]['теги']:
                notes_filtered[key] = notes[key]
        button6.setText('Отмена')
        list_widget1.clear()
        list_widget2.clear()
        text_edit.clear()
        list_widget1.addItems(notes_filtered)
    else:
        list_widget1.clear()
        list_widget1.addItems(notes)
        line_edit.clear()
        button6.setText('Искать заметки по тегу')


app = QApplication([])

window = QWidget()
window.setWindowTitle('Умные заметки')
window.resize(900, 600)

main_hline = QHBoxLayout()
vline_1 = QVBoxLayout()
vline_2 = QVBoxLayout()
hline_1 = QHBoxLayout()
hline_2 = QHBoxLayout()

text_edit = QTextEdit()
list_name = QLabel('Список заметок')
tags_name = QLabel('Список тегов')
button1 = QPushButton('Создать заметку')
button2 = QPushButton('Удалить заметку')
button3 = QPushButton('Сохранить заметку')
button4 = QPushButton('Добавить к заметке')
button5 = QPushButton('Открепить от заметки')
button6 = QPushButton('Искать заметки по тегу')
list_widget1 = QListWidget()
list_widget2 = QListWidget()
line_edit = QLineEdit()
line_edit.setPlaceholderText('Введите тег:')

hline_1.addWidget(button1)
hline_1.addWidget(button2)

hline_2.addWidget(button4)
hline_2.addWidget(button5)

vline_1.addWidget(text_edit)

vline_2.addWidget(list_name)
vline_2.addWidget(list_widget1)
vline_2.addLayout(hline_1)
vline_2.addWidget(button3)
vline_2.addWidget(tags_name)
vline_2.addWidget(list_widget2)
vline_2.addWidget(line_edit)
vline_2.addLayout(hline_2)
vline_2.addWidget(button6)

main_hline.addLayout(vline_1)
main_hline.addLayout(vline_2)

window.setLayout(main_hline)

with open('notes_data.json','r') as file:
    notes = json.load(file)

list_widget1.addItems(notes)
list_widget1.itemClicked.connect(show_note)

button1.clicked.connect(add_note)
button2.clicked.connect(del_note)
button3.clicked.connect(save_note)

button4.clicked.connect(add_tag)
button5.clicked.connect(del_tag)
button6.clicked.connect(search_tag)

window.show()
app.exec_()
