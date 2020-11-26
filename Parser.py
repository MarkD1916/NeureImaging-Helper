import openpyxl

class Parser():
    def __init__(self):
        pass

    def getDataFromColumnXlsx(self, sh, decodingColumn):
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
                workbook = openpyxl.load_workbook(path,data_only=True)
                sh = workbook["Sheet1"]
                # get boundary
                for cellName, bordersSize in zip(TrepanationWindowBordersNameCell,TrepanationWindowBordersSizeCell):
                    fileInfo[sh[cellName].value]=sh[bordersSize].value
                for k, column in zip(fileInfo.keys(),["C","B","E","F"]):
                    fileInfo[k] = self.getDataFromColumnXlsx(sh=sh,decodingColumn=column)
            else:
                for k in fileInfo.keys():
                    fileInfo[k] = ["No file"]
            InfoID[ID] = fileInfo
        return InfoID