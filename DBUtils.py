import sqlite3
import os.path
import string


class Utils():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'NBDB.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def selectAllFromTable(self, tableName, field="*"):
        sql = "SELECT {} FROM {}".format(field, tableName)
        self.cursor.execute(sql)
        return  self.cursor.fetchall()



    def insertDataInTable(self,tableName,data):
        types = ["?" for i in range(len(data[0]))]
        print(types)
        self.cursor.executemany("INSERT INTO {} VALUES {}".format(tableName,"("+",".join(types)+")"), data)
        self.conn.commit()


    def dropTable(self, tableName):
        self.cursor.execute('drop table if exists ' + tableName)
        self.conn.commit()

    def createTable(self,tableName,*args):
        self.cursor.execute("""CREATE TABLE {}
                           ({})
                        """.format(tableName,*args))
        self.conn.commit()


U = Utils()
#U.createTable("Rat","RatID INTEGER PRIMARY KEY , Name text NOT NULL, Mass text NOT NULL")
U.insertDataInTable("Rat",[(None,"ФИ-113","500"),(None,"ФИ-11","504"),(None,"ФИ-1","500")])
#U.dropTable("Rat")
print(U.selectAllFromTable("Rat"))
# Создание таблицы
# cursor.execute("""CREATE TABLE Date
#                   (date text, rat text)
#                """)
#cursor.executemany("INSERT INTO date VALUES (?,?)", np.transpose([dates,names]))
# conn = sqlite3.connect('NBDB.db')
# cursor = conn.cursor()
# sql = "SELECT date FROM Date"
# cursor.execute(sql)
# print(cursor.fetchall()) # or use fetchone()

