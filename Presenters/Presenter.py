from Initializer import InitializerDB
from DBUtils import Utils
import numpy as np
class InitPresenter():
    def __init__(self):
        self.utils=None

    def createNewDatabase(self,dbPath,dbName):
        Init = InitializerDB(dbPath,dbName)
        Init.getExperiments()
        Init.getRoiLLMData()
        Init.createTables()
        Init.insertDataInDB()
        self.utils = Init.getDB()
        return self.utils

    def getDrugs(self,utils = None):
        if self.utils==None:
            self.utils = utils
        drugs = np.ravel(self.utils.selectFromExpAndMetaExp("DrugName", "Drugs"))
        return drugs

    def getName(self,utils = None):
        if self.utils==None:
            self.utils = utils
        name = np.ravel(self.utils.selectAllFromTable("Experiments", "Name"))
        return name

