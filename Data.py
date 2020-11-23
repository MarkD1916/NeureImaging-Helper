import os
import re
#import docx
import numpy as np
import docx2txt
import openpyxl

class Searcher():

    def __init__(self,mainDir):
        self.mainDir = mainDir
        self.topLevelName = []
        self.drugsList=[]
        self.date = []
        self.TrepanationWindowBordersNameCell = ["G2","G3","G4","G5"]
        self.TrepanationWindowBordersSizeCell = ["H2", "H3", "H4", "H5"]
        self.ROILLMFiles = []

    def getDrugsList(self):
        drugsList = np.loadtxt("./drugsFile.txt",dtype='str',delimiter='\t')
        self.drugsList = drugsList

    def searchDataFolderName(self):
        self.topLevelName = [re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+",name).group(0)
                          for name in os.listdir(self.mainDir) if
             os.path.isdir(os.path.join(self.mainDir, name))
                        and re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+",name) is not None]


        return self.topLevelName

    def searchDateData(self):
        date = [re.match(r"(\d+.\d+.\d+)", name).group(0)
                        for name in os.listdir(self.mainDir) if
                        os.path.isdir(os.path.join(self.mainDir, name))
                        and re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+", name) is not None]
        self.date = date

        return date

    def searchRatName(self):
        name = [''.join(re.findall(r"([А-Я]+|[а-я]+)(\-)([1-9]+)", name)[0])
                for name in os.listdir(self.mainDir) if
                os.path.isdir(os.path.join(self.mainDir, name))
                and len(re.findall(r"([А-Я]+|[а-я]+)(\-)([1-9]+)", name))>0

                ]
        return name

    def searchCoordData(self):
        return

    def searchDrugsData(self):
        AllDrugs=[]
        for folderName in self.topLevelName:
            path = os.path.join(self.mainDir,folderName)
            for i in self.walklevel(path,level=0):
                Drugs = []
                for prot in i[-1]:

                    if "Протокол от " in prot:

                        text = docx2txt.process(os.path.join(path,prot))
                        text_drugs = text[text.find(u"Вещество"):text.find(u"Вещество") + 300]
                        for i,j in zip(np.unique(self.drugsList),range(len(self.drugsList))):
                            if i.strip() in text_drugs:
                                Drugs.append(i.strip())
                        if len(re.findall(r"[1-9]\n", text_drugs))>len(np.unique(Drugs)):
                            Drugs.append("Есть неизвестные вещества")
                        AllDrugs.append(np.unique(Drugs))
                if len(Drugs) == 0:
                    AllDrugs.append(["Не обнаружен протокол"])

        return AllDrugs


    def walklevel(self,some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def searchRoiLLMFile(self):
        for folderName,d in zip(self.topLevelName,self.date):
            path = os.path.join(self.mainDir,folderName,d+"_coordinates","prog",d+"_ROI_LLM.xlsx")
            print(path)
            try:
                workbook = openpyxl.load_workbook(path,data_only=True)
                self.ROILLMFiles.append(path)
            except FileNotFoundError:
                self.ROILLMFiles.append("No file")
        return self.ROILLMFiles

    def searchBounderyData(self):
        bounderyInfoID = {}
        borders = []
        for path, ID in zip(self.ROILLMFiles,range(1,len(self.ROILLMFiles)+1)):
            if path!="No file":
                bordersSizeList = [[], []]
                workbook = openpyxl.load_workbook(path,data_only=True)
                sh = workbook["Sheet1"]
                for cellName, bordersSize in zip(self.TrepanationWindowBordersNameCell,self.TrepanationWindowBordersSizeCell):
                    bordersSizeList[0].append(sh[cellName].value)
                    bordersSizeList[1].append(str(sh[bordersSize].value))
                bounderyInfoID[ID] = bordersSizeList
            # else:
            #     bordersSizeList[0].append("No ROI_LLM file")
            #     bordersSizeList[1].append("No ROI_LLM file")
            #     bordersSizeList[0] = bordersSizeList[0] * 4
            #     bordersSizeList[1] = bordersSizeList[1] * 4
            #borders.append(bordersSizeList)

        return bounderyInfoID

    def searchCoordsInfo(self):
        coordsInfoID={}
        for path,ID in zip(self.ROILLMFiles,range(1,len(self.ROILLMFiles)+1)):
            coordsInfo = {}
            decodingColumnDrugName = "C"
            if path != "No file":
                workbook = openpyxl.load_workbook(path, data_only=True)
                sh = workbook["Sheet1"]
                val = 2
                drugsNameList=[]
                while val!=None:
                    drugName = sh[decodingColumnDrugName+str(val)].value
                    if drugName==None:
                        break
                    drugsNameList.append(drugName)
                    val+=1
                coordsInfoID[ID] = drugsNameList
        return coordsInfoID




Search = Searcher(mainDir="D:/N_img")
Search.searchDataFolderName()
Search.searchDateData()
Search.searchRoiLLMFile()
print(Search.searchBounderyData())
Search.searchCoordsInfo()