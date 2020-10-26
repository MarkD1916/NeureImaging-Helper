import sqlite3
import os.path




class Utils():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'NBDB.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def selectAllFromDate(self):
        sql = "SELECT * FROM Date"
        self.cursor.execute(sql)
        return  self.cursor.fetchall()

    def insertDate(self,data):

        self.cursor.executemany("INSERT INTO date VALUES (?,?)", data)
        self.conn.commit()

    def deleteDateByDate(self,date):
        pass

    def deleteDateByName(self,name):
        pass

    def deleteDateByNameDate(self,data):
        pass

    def dropTable(self, tableName):
        self.cursor.execute('drop table if exists ' + tableName)
        self.conn.commit()

    def createTable(self,tableName,*args):
        self.cursor.execute("""CREATE TABLE {}
                           ({})
                        """.format(tableName,*args))
        self.conn.commit()



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

