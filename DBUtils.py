import sqlite3
import os.path
import numpy as np



class Utils(object):
    cursor = None
    def __init__(self,db_path=None):
        if Utils.cursor is None and db_path!=None:
            self.conn = sqlite3.connect(db_path,check_same_thread = False)
            self.cursor = self.conn.cursor()

    def selectAllFromTable(self, tableName, field="*"):
        sql = "SELECT {} FROM {}".format(field, tableName)
        self.cursor.execute(sql)
        return  self.cursor.fetchall()

    def getDBPath(self):
        path = self.db_path
        return path

    def selectFromExpAndMetaExp(self,field,table):
        sql = "SELECT DISTINCT {} FROM Experiments,{} WHERE Experiments.ID=ExpId".format(field,table)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectExpByDrugs(self, drugsFields):
        drugsFields = ["'"+d+"'" for d in drugsFields]
        drugsFields = ' or DrugName LIKE '.join(drugsFields)
        sql = "SELECT DISTINCT Name FROM Experiments,Drugs where (DrugName LIKE {}) and Experiments.ID=ExpId".format(drugsFields)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insertDataInTable(self,tableName,data):
        types = ["?" for i in range(len(data[0]))]
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

    def selectFieldFromTable(self,field,tableName):
        sql = "SELECT {} FROM {}".format(field, tableName)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectBoundaryForExp(self,selectedExpID):
        selectedExpID = ["'" + str(d) + "'" for d in selectedExpID]
        selectedExpID = ' or ExpID='.join(selectedExpID)
        sql = "SELECT DISTINCT Rostral,Caudal,Medial,Lateral,ExpID FROM Experiments,Boundary where ExpID={}".format(selectedExpID)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectCoordsForExp(self,selectedExpID,selectedDrugs):
        selectedExpID = ["'" + str(d) + "'" for d in selectedExpID]
        selectedExpID = ' or Cords.ExpID='.join(selectedExpID)
        selectedDrugs = ["'" + str(d) + "'" for d in selectedDrugs]
        selectedDrugs = ' or DrugName LIKE '.join(selectedDrugs)

        sql = "select xValue,yValue,ID,ExpID from Cords " \
              "where ID in (select ID from Drugs where DrugName LIKE {}) and (Cords.ExpID={}) order by Cords.ID".format(selectedDrugs,selectedExpID)
        print (sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectExpIDByName(self,selectedName):
        selectedName = ["'" + str(d) + "'" for d in selectedName]
        selectedName = ' or name='.join(selectedName)
        sql = "SELECT ID FROM Experiments where Name={}".format(
            selectedName)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectDrugsNameByID(self,idS):
        selectedidS = ["'" + str(d) + "'" for d in idS]
        selectedidS = ' or ID='.join(selectedidS)
        sql = "SELECT DrugName FROM Drugs where ID={} order by ID".format(
            selectedidS)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectAllExpAndDrugs(self):
        sql = "SELECT DISTINCT Name,DrugName FROM Experiments,Drugs where Experiments.ID=ExpId"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectAllDrugs(self):
        sql = "SELECT DISTINCT DrugName FROM Drugs"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def selectExpNoFiles(self):
        sql = "SELECT DISTINCT Path,Date,ExpId FROM Experiments,Drugs where Experiments.ID=ExpId and DrugName LIKE 'Файл не найден'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    # update записей в таблицах БД из ROI файла
    def delDataByNewFile(self,idForDel,dataForUpdate):
        for tableName in ["Cords","Drugs","Cords"]:
            print (tableName)


            if tableName=="Boundary":
                for boundaryKey in ["rostral", "caudal", "medial", "lateral"]:
                    sql_for_update = "UPDATE {} SET {}={} WHERE ExpId={}".format(tableName,boundaryKey,dataForUpdate[idForDel][boundaryKey],idForDel)
                    self.cursor.execute(sql_for_update)
                    self.conn.commit()


            if tableName == "Drugs":
                sql = "SELECT * from {} where ExpId={}".format(tableName, idForDel)
                self.cursor.execute(sql)
                startId = self.cursor.fetchall()[0][0]
                sql_delete = 'DELETE FROM {} WHERE ExpId = {}'.format(tableName,idForDel)
                self.cursor.execute(sql_delete)
                self.conn.commit()

                lenInsertedData = len(dataForUpdate[idForDel]["drugName"])
                for id,expid,drugname,valve in zip(range(startId,lenInsertedData+startId),[idForDel]*lenInsertedData,dataForUpdate[idForDel]["drugName"],dataForUpdate[idForDel]["valve"]):
                    data = (id,expid,drugname,valve)
                    types = ["?" for i in range(len(data))]
                    self.cursor.executemany("INSERT INTO {} VALUES {}".format(tableName,"("+",".join(types)+")"), [data])
                    self.conn.commit()
                sql = "SELECT * from {} where ExpId={}".format(tableName, idForDel)
                self.cursor.execute(sql)


            if tableName == "Cords":
                sql = "SELECT * from {} where ExpId={}".format(tableName, idForDel)
                self.cursor.execute(sql)
                startId = self.cursor.fetchall()[0][0]
                sql_delete = 'DELETE FROM {} WHERE ExpId = {}'.format(tableName, idForDel)
                self.cursor.execute(sql_delete)
                self.conn.commit()

                lenInsertedData = len(dataForUpdate[idForDel]["xValue"])
                for id, xValue, yValue,expId in zip(range(startId, lenInsertedData + startId),
                                                      dataForUpdate[idForDel]["xValue"],
                                                        dataForUpdate[idForDel]["yValue"],
                                                      [idForDel] * lenInsertedData, ):
                    data = (id, xValue, yValue, expId)
                    types = ["?" for i in range(len(data))]
                    self.cursor.executemany("INSERT INTO {} VALUES {}".format(tableName, "(" + ",".join(types) + ")"),
                                            [data])
                    self.conn.commit()
            sql = "SELECT * from {} where ExpId={}".format(tableName, idForDel)
            self.cursor.execute(sql)
        return

    def selectFolderInBD(self):
        sql = "SELECT Path FROM Experiments"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def addNewExp(self, dataForInsert,dataForExpInsertFile):
        sql = "SELECT max(ID) from Experiments"
        self.cursor.execute(sql)

        lastID = self.cursor.fetchall()[0][0]+1

        dataForInsert = list(dataForInsert)

        dataForInsert.insert(0, lastID)

        types = ["?" for i in range(len(dataForInsert))]
        self.cursor.executemany("INSERT INTO {} VALUES {}".format("Experiments", "(" + ",".join(types) + ")"),
                                [dataForInsert])
        self.conn.commit()



        for tableName in ["Cords","Drugs","Cords","Boundary"]:

            if tableName=="Boundary":
                boundaryData = []
                for boundaryKey in ["rostral", "caudal", "medial", "lateral"]:

                    getData = dataForExpInsertFile[1][boundaryKey]
                    boundaryData.append(getData)
                boundaryData.append(lastID)
                sql = "SELECT max(ID) from Boundary"
                self.cursor.execute(sql)

                lastIDBoundary = self.cursor.fetchall()[0][0] + 1
                #print (lastIDBoundary)
                boundaryData.insert(0,lastIDBoundary)
                types = ["?" for i in range(len(boundaryData))]
                self.cursor.executemany("INSERT INTO {} VALUES {}".format("Boundary", "(" + ",".join(types) + ")"),
                                        [boundaryData])
                self.conn.commit()
            if tableName == "Drugs":
                sql = "SELECT max(ID) from Drugs"
                self.cursor.execute(sql)

                lastIDDrugs = self.cursor.fetchall()[0][0] + 1
                # print (lastIDBoundary)
                lenInsertedData = len(dataForExpInsertFile[1]["drugName"])
                for id,expid,drugname,valve in zip(range(lastIDDrugs,lenInsertedData+lastIDDrugs),[lastID]*lenInsertedData,dataForExpInsertFile[1]["drugName"],dataForExpInsertFile[1]["valve"]):
                    data = (id,expid,drugname,valve)
                    types = ["?" for i in range(len(data))]
                    self.cursor.executemany("INSERT INTO {} VALUES {}".format("Drugs", "(" + ",".join(types) + ")"),
                                            [data])
                    self.conn.commit()



            if tableName == "Cords":
                sql = "SELECT max(ID) from Cords"
                self.cursor.execute(sql)

                lastIDCords = self.cursor.fetchall()[0][0] + 1
                lenInsertedData = len(dataForExpInsertFile[1]["xValue"])
                for id, xValue, yValue,expId in zip(range(lastIDCords, lenInsertedData + lastIDCords),
                                                      dataForExpInsertFile[1]["xValue"],
                                                        dataForExpInsertFile[1]["yValue"],
                                                      [lastID] * lenInsertedData, ):
                    data = (id, xValue, yValue, expId)
                    print (data)
                    types = ["?" for i in range(len(data))]
                    self.cursor.executemany("INSERT INTO {} VALUES {}".format("Cords", "(" + ",".join(types) + ")"),
                                            [data])
                    self.conn.commit()

        sql = "SELECT * from Experiments"
        self.cursor.execute(sql)
        print(self.cursor.fetchall())

        sql = "SELECT * from Boundary where ExpID = 13"
        self.cursor.execute(sql)
        print(self.cursor.fetchall())

        sql = "SELECT * from Drugs where ExpID = 13"
        self.cursor.execute(sql)
        print(self.cursor.fetchall())

        sql = "SELECT * from Cords where ExpID = 13"
        self.cursor.execute(sql)
        print(self.cursor.fetchall())

        return

    def returnNewExpID(self):
        sql = "SELECT max(ID) from Experiments"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]+1

    # def insertDataFromFile(self):
    #     for tableName in ["Cords","Drugs","Cords"]:
    #         print (tableName)
    #
    #         if tableName=="Boundary":
    #             for boundaryKey in ["rostral", "caudal", "medial", "lateral"]:
    #                 sql_for_update = "UPDATE {} SET {}={} WHERE ExpId={}".format(tableName,boundaryKey,dataForUpdate[idForDel][boundaryKey],idForDel)
    #                 self.cursor.execute(sql_for_update)
    #                 self.conn.commit()




# U = Utils()
# # Ищем необходимые поля
# Search = Searcher(mainDir="D:/N_img")
# Search.searchDateData()
# path,name = Search.searchExpPath()
# Search.searchRoiLLMFile()
# Search.parseRoiLlmFile()
# methodCalc = Search.searchExpMethod()
# print(Search.searchRoiLLMFile())
# drugs = Search.searchDrugs()
# valves = Search.searchValve()
#print (path)
#print (methodCalc)
# U.dropTable("Drugs")
# U.dropTable("Cords")
# U.dropTable("Experiments")
# U.dropTable("Boundary")
# for p,n in zip(path,name):
#    U.insertDataInTable("Experiments",[(None,p,n)])
# print(drugs)
# print (valves)

# for d in drugs.keys():
#     for val in range(len(drugs[d])):
#         v = valves[d][val]
#         if v==3:
#             v = None
#         #print (v)
#         U.insertDataInTable("Drugs",[(None,drugs[d][val],d,v)])
# print (U.selectAllFromTable("Experiments"))
#
#U.createTable("Experiments","ID INTEGER PRIMARY KEY , Path text NOT NULL, Name text NOT NULL, Date text NOT NULL")
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
# U.createTable("Drugs",
#              "ID INTEGER PRIMARY KEY ,\
#               ExpId INTEGER NOT NULL,\
#               DrugName text NOT NULL,\
#               Valve INTEGER,\
#               FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")
#
# U.createTable("Cords",
#              "ID INTEGER PRIMARY KEY ,\
#               xValue REAL,\
#               yValue REAL,\
#               Region Text,\
#               ExpId INTEGER NOT NULL,\
#               FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")






