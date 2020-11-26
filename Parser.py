import openpyxl

class Parser():
    def __init__(self):
        pass

    def getDataFromXlsx(self, sh, decodingColumn):
        val = 2
        drugsNameList = []
        while val != None:
            drugName = sh[decodingColumn + str(val)].value
            if drugName == None:
                break
            drugsNameList.append(drugName)
            val += 1
        return drugsNameList

    def pullNoneIndata(self, info):
        lenColumns = []
        for k in info.keys():
            lenColumns.append(len(info[k]))
        return

    def parseRoiLlmFile(self,ROILLMFiles):
        InfoID = {}
        for path, ID in zip(ROILLMFiles,range(1,len(ROILLMFiles)+1)):
            fileInfo={"Drug":[],"Valve":[],"xValue":[],"yValue":[],"Rostral":[],"Caudal":[],"Medial":[],"Lateral":[]}
            TrepanationWindowBordersNameCell = ["G2", "G3", "G4", "G5"]
            TrepanationWindowBordersSizeCell = ["H2", "H3", "H4", "H5"]

            if path!="No file":
                bordersSizeList = [[], []]
                workbook = openpyxl.load_workbook(path,data_only=True)
                sh = workbook["Sheet1"]
                # get boundary
                for cellName, bordersSize in zip(TrepanationWindowBordersNameCell,TrepanationWindowBordersSizeCell):
                    bordersSizeList[0].append(sh[cellName].value)
                    bordersSizeList[1].append(str(sh[bordersSize].value))
                    fileInfo[sh[cellName].value]=sh[bordersSize].value
                # get Drugs
                drugsNameList = self.getDataFromXlsx(sh=sh,decodingColumn="C")
                fileInfo["Drug"] = drugsNameList
                # get valves
                valves = self.getDataFromXlsx(sh=sh,decodingColumn="B")
                fileInfo["Valve"] = valves
                #get xValues
                xValues = self.getDataFromXlsx(sh=sh,decodingColumn="E")
                fileInfo["xValue"] = xValues
                #get yValues
                yValues = self.getDataFromXlsx(sh=sh, decodingColumn="F")
                fileInfo["yValue"] = yValues
            else:
                pass
            InfoID[ID] = fileInfo
        #print(InfoID)
        return InfoID