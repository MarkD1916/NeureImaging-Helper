from Data import Searcher
from Parser import Parser
from DBUtils import Utils
#"D:/N_img"
class InitializerDB():

    def __init__(self,mainDir):
        self.search = Searcher(mainDir=mainDir)
        self.parser = Parser()
        self.experiments = []
        self.drugs = []
        self.cords = {"ID":[],"expID":[],"xValue":[],"yValue":[],"region":[]}
        self.boundary = {"ID":[],"expID":[],"Rostral":[],"Caudal":[],"Medial":[],"Lateral":[]}
        self.rat = {}

    def getExperiments(self):
        metaData = {"ID":[],"path":[],"name":[],"date":[]}
        date = self.search.searchDateData()
        path,name = self.search.searchExpPath()
        metaData["path"] = path
        metaData["name"] = name
        metaData["date"] = date
        metaData["ID"] = [x for x in range(1,len(path)+1)]
        self.experiments = metaData

    def setExperimentsDataInDB(self):
        pass

    def makeRowForTable(self,data, keys):



        return

    def getRoiLLMData(self):
        filesPath = self.search.searchRoiLLMFile()
        roiLLMData = self.parser.parseRoiLlmFile(filesPath)
        drugsTableData=self.makeRowForTable(roiLLMData,['Drug','Valve'])
        self.drugs = drugsTableData

Init = InitializerDB("/mnt/data/N_img")
Init.getExperiments()
Init.getRoiLLMData()