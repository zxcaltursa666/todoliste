# import libraries
import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

import sqlite3

# creating a database
conn = sqlite3.connect('todolist.db')
# creating a cursor
cur = conn.cursor()
# creating table
cur.execute("""CREATE TABLE if not exists to_do_list(
    item text
    )""")
# commit
conn.commit()
# close connection
conn.close()


# initializing our window
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('listodo.ui', self)
        self.Add.clicked.connect(self.adding)
        self.Delete.clicked.connect(self.deleting)
        self.Clear.clicked.connect(self.clearing)
        self.Save.clicked.connect(self.saving)
        self.database()

    # adding function
    def adding(self):
        item = self.lineEdit.text()

        self.ListShow.addItem(item)

        self.lineEdit.setText("")

    # deleting function
    def deleting(self):
        chosen = self.ListShow.currentRow()
        self.ListShow.takeItem(chosen)

    # clearing function
    def clearing(self):
        self.ListShow.clear()

    # saving function
    def saving(self):
        # creating a database
        conn = sqlite3.connect('todolist.db')
        # creating a cursor
        cur = conn.cursor()
        # clearing table
        cur.execute('DELETE FROM to_do_list;',)

        tasks = []
        # appending our list
        for index in range(self.ListShow.count()):
            tasks.append(self.ListShow.item(index))
        # inserting values in table
        for i in tasks:
            cur.execute("INSERT INTO to_do_list VALUES (:i)",
                        {
                            'i': i.text(),
                        })
        # commit
        conn.commit()
        # close connection
        conn.close()

    def database(self):
        # creating a database
        conn = sqlite3.connect('todolist.db')
        # creating a cursor
        cur = conn.cursor()
        # selecting all from table
        cur.execute("SELECT * FROM to_do_list")
        # fetchall will return a list of tuples
        fetch = cur.fetchall()
        # commit
        conn.commit()
        # close connection
        conn.close()
        # returning information in QListWidget(str)
        for v in fetch:
            self.ListShow.addItem(str(v[0]))


# making a point of entry
if __name__ == '__main__':
    ex = QApplication(sys.argv)
    app = App()
    app.show()
    sys.exit(ex.exec())
