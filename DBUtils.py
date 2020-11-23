import sqlite3
import os.path
import string
from Data import Searcher

class Utils():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(BASE_DIR, 'NBDB.db')
        print(self.db_path)
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
Search = Searcher(mainDir="D:/N_img")
Search.searchDataFolderName()
date = Search.searchDateData()
name = Search.searchRatName()
#
Search.searchRoiLLMFile()
boundary = Search.searchBounderyData()
cordsDrugName = Search.searchCoordsInfo()
print (cordsDrugName)
# #U.createTable("Rat","RatID INTEGER PRIMARY KEY , Name text NOT NULL, Mass text NOT NULL")
# U.createTable("Experiments","ID INTEGER PRIMARY KEY , Name text NOT NULL, Date text NOT NULL")
# U.createTable("Boundary",
#               "BoundaryID INTEGER PRIMARY KEY , BoundaryName text NOT NULL, BoundaryValue text NOT NULL,ExpId INTEGER NOT NULL,FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")
# U.createTable("ExperimentsMetaData",
#              "MetaDataID INTEGER PRIMARY KEY , Drug text NOT NULL,ExpId INTEGER NOT NULL,FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")
# for date, name in zip(date,name):
#     print (name,date)
#     U.insertDataInTable("Experiments",[(None,name,date)])
# for k in cordsDrugName.keys():
#     for val in cordsDrugName[k]:
#         U.insertDataInTable("ExperimentsMetaData",[(None,val,k)])
# for k in boundary.keys():
#     for val1,val2 in zip(boundary[k][0],boundary[k][1]):
#         U.insertDataInTable("Boundary",[(None,val1,val2,k)])

#U.dropTable("Rat")
# U.dropTable("Boundary")
# U.dropTable("ExperimentsMetaData")



#print(U.selectAllFromTable("ExperimentsMetaData"))
#print(U.selectAllFromTable("Experiments"))
#print(U.selectFromExpAndMetaExp("Drug"))
#print(U.selectAllFromTable("Experiments","Name"))


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

