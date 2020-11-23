# coding=utf-8
from tkinter import *
from DBUtils import Utils
import numpy as np
import sqlite3
from Presenters.Presenter import PlotPresenter
class mainWindow(Utils):
    db_path = Utils().db_path

    def __init__(self,root):
        self.TrepanationWindowBordersNameCell = ["G2", "G3", "G4", "G5"]
        self.TrepanationWindowBordersSizeCell = ["H2", "H3","H4", "H5"]
        self.db_path = self.getDBPath()
        print(self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.root = root
        self.root.title("NeuroImagingHelper")
        self.root.geometry("660x300")
        self.data = []
        self.root.resizable(width=False, height=False)
        self.ROILLMFiles = []
        self.listboxName = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#c3f8fa')
        self.listboxName.place(x=10, y=32)
        self.listboxName.config()

        self.listboxDate = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#c3f8fa')
        self.listboxDate.place(x=150, y=32)
        self.listboxDate.config()

        self.listboxDrugs = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#c3f8fa')
        self.listboxDrugs.place(x=290, y=32)
        self.listboxDrugs.config()

        self.listboxDrugsForPlot = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#c3f8fa')
        self.listboxDrugsForPlot.place(x=10, y=164)
        self.listboxDrugsForPlot.config()

        self.prev_button = Button(text=u"Построить график", background='#d8e1e1',command=self.new_window)
        self.prev_button.place(x=440, y=32)
        self.prev_button.config()

        #self.dirs = self.searchDataFolderName()

        self.idx = 0
        self.idxDate = 0
        self.idxDrugs = 0


        self.drugs = np.ravel(self.selectFromExpAndMetaExp("Drug"))
        self.name = np.ravel(self.selectAllFromTable("Experiments","Name"))
        print (self.drugs)

        #self.Boundery = self.searchBounderyData()
        #self.coordsInfo = self.searchCoordsInfo()


        self.selectedRatsByDrugs = range(len(self.name))

        self.g_i()
        self.selectName()

        #self.g_i_Date()
        #self.selectDate()

        self.g_i_Drugs()

        self.root.configure(background='#fdfbfb')
        # self.root.mainloop()

    def selectName(self, *args):
        value_name = [self.listboxName.get(idx) for idx in self.listboxName.curselection()]
        value_idx = [idx for idx in self.listboxName.curselection()]
        if len(value_name) == 0:
            self.listboxName.select_set(0)
            value_name = [self.listboxName.get(0)]
            value_idx = [0]
        self.idx = value_idx
        print (self.idx, "Name index")
        return value_name, value_idx

    def g_i(self, nameSelectedByDrugs=None):
        if nameSelectedByDrugs!=None:
            name = nameSelectedByDrugs
        else:
            name=self.name
        self.listboxName.delete(0, 'end')
        itemList = np.array(name)
        for item in itemList:
            self.listboxName.insert(END, item)
        self.listboxName.bind('<<ListboxSelect>>', self.selectName)
        self.listboxName.select_set(0)
        self.listboxName.event_generate("<<ListboxSelect>>")


    def selectDrugs(self, *args):
        self.selectedRatsByDrugs = []
        value_name = [self.listboxDrugs.get(idx) for idx in self.listboxDrugs.curselection()]
        value_idx = [idx for idx in self.listboxDrugs.curselection()]
        if len(value_name) == 0:
            self.listboxDrugs.select_set(0)
            value_name = [self.listboxDrugs.get(0)]
            value_idx = [0]
        selectedDrugs = value_name
        self.idxDrugs = value_idx

        ratNames = self.selectExpByDrugs(drugsFields=self.drugs[self.idxDrugs])
        self.g_i(ratNames)
        return value_name, value_idx

    def g_i_Drugs(self):
        self.listboxDrugs.delete(0, 'end')
        for item in self.drugs:
            self.listboxDrugs.insert(END, item)
        self.listboxDrugs.bind('<<ListboxSelect>>', self.selectDrugs)
        self.listboxDrugs.select_set(0)
        self.listboxDrugs.event_generate("<<ListboxSelect>>")

    def new_window(self):
        self.newWindow = Tk()
        self.app = plotWindow(self.newWindow,str(self.idx))

    def plotBoundery(self):
        boundary = np.array(self.Boundery)[self.selectedRatsByDrugs][self.idx]
        Rostral = float(boundary[0][1][0])
        Caudal = float(boundary[0][1][1])
        Medial = float(boundary[0][1][2])
        Lateral = float(boundary[0][1][3])
        # plt.scatter(Caudal,Medial,color='green')
        # plt.scatter(Rostral,Medial,color='green')
        # plt.scatter(Caudal,Lateral,color='green')
        # plt.scatter(Rostral,Lateral,color='green')
        # xCR = np.linspace(Caudal,Rostral,num=5)
        # yCR = [Medial]*5
        # xCL = [Caudal]*5
        # yCL = np.linspace(Medial,Lateral,num=5)
        # xLR = np.linspace(Caudal,Rostral,num=5)
        # yLR = [Lateral]*5
        # xRL = [Rostral]*5
        # yRL = np.linspace(Medial,Lateral,num=5)
        # plt.plot(xCR,yCR,color='blue')
        # plt.plot(xCL,yCL,color='blue')
        # plt.plot(xLR,yLR,color='blue')
        # plt.plot(xRL,yRL,color='blue')
        # plt.show()
        return

class plotWindow():
    def __init__(self, root, name):
        self.root = root
        self.root.title(name)
        self.root.geometry("660x300")
        self.frame = Frame(self.root)
        self.update_button = Button(self.root,text=u"Обновить график", background='#d8e1e1', command=self.newData)
        self.update_button.place(x=440, y=32)
        self.frame.place()
        self.update_button.config()


    def newData(self):
        print (PlotPresenter().currentData)

#A = app()
def main():
    root = Tk()
    app = mainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()