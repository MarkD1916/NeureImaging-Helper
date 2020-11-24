import sqlite3
import os.path
import string
from Data import Searcher

class Utils():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(BASE_DIR, 'NBDB.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()



    def selectAllFromTable(self, tableName, field="*"):
        sql = "SELECT {} FROM {}".format(field, tableName)
        self.cursor.execute(sql)
        return  self.cursor.fetchall()

    def getDBPath(self):
        path = self.db_path
        return path

    def selectFromExpAndMetaExp(self,field):
        sql = "SELECT DISTINCT {} FROM Experiments,ExperimentsMetaData WHERE ID=ExpId".format(field)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectExpByDrugs(self, drugsFields):
        drugsFields = ["'"+d+"'" for d in drugsFields]
        drugsFields = ' or Drug LIKE '.join(drugsFields)
        sql = "SELECT DISTINCT Name FROM Experiments,ExperimentsMetaData where (Drug LIKE {}) and ID=ExpId".format(drugsFields)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
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
Search = Searcher(mainDir="/mnt/data/N_img")
Search.searchDateData()

path,name = Search.searchExpPath()
methodCalc = Search.searchExpMethod()
print(Search.searchRoiLLMFile())
drugs = Search.searchDrugs()
valves = Search.searchValve()
#print (path)
#print (methodCalc)
# U.dropTable("Drugs")
#U.dropTable("Boundary")
#U.dropTable("Experiments")
#for p,n in zip(path,name):
#    U.insertDataInTable("Experiments",[(None,p,n)])
print(drugs)
print (valves)

# for d in drugs.keys():
#     for val in range(len(drugs[d])):
#         v = valves[d][val]
#         if v==3:
#             v = None
#         #print (v)
#         U.insertDataInTable("Drugs",[(None,drugs[d][val],d,v)])
# print (U.selectAllFromTable("Drugs"))
#
#U.createTable("Experiments","ID INTEGER PRIMARY KEY , Path text NOT NULL, Name text NOT NULL")
#
# U.createTable("Rat","ID INTEGER PRIMARY KEY , Name text NOT NULL, Mass text NOT NULL,ExpId INTEGER NOT NULL,FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")
#
# U.createTable("Boundary",
#               "ID INTEGER PRIMARY KEY ,\
#               Rostral text NOT NULL,\
#               Caudal text NOT NULL, \
#               Medial text NOT NULL, \
#               Lateral text NOT NULL,\
#               ExpId INTEGER NOT NULL,FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")
#
U.createTable("Drugs",
             "ID INTEGER PRIMARY KEY ,\
              DrugName text NOT NULL,\
              ExpId INTEGER NOT NULL,\
              Valve INTEGER,\
              FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")
#
# U.createTable("Cords",
#              "ID INTEGER PRIMARY KEY ,\
#               xValue REAL,\
#               yValue REAL,\
#               Region Text,\
#               ExpId INTEGER NOT NULL,\
#               FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")






