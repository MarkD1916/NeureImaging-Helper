# coding=utf-8
from tkinter import *
from tkinter import filedialog,simpledialog
from DBUtils import Utils
import numpy as np
import time
import threading
from Presenters.Presenter import InitPresenter,ObserverPresenter,PlotPresenter
from Views.InsertView import InsertWindow
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


class mainWindow():

    def __init__(self,root):
        self.initPresenter = InitPresenter()
        self.initFlag = False
        self.TrepanationWindowBordersNameCell = ["G2", "G3", "G4", "G5"]
        self.TrepanationWindowBordersSizeCell = ["H2", "H3","H4", "H5"]
        self.root = root
        self.root.title("NeuroImagingHelper")
        self.root.geometry("660x300")
        self.data = []
        self.root.resizable(width=False, height=False)
        self.ROILLMFiles = []
        self.listboxName = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#33aafd')
        self.listboxName.place(x=10, y=32)
        self.listboxName.config()

        # self.listboxDate = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#33aafd')
        # self.listboxDate.place(x=150, y=32)
        # self.listboxDate.config()

        self.listboxDrugs = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#33aafd')
        self.listboxDrugs.place(x=290, y=32)
        self.listboxDrugs.config()

        # self.listboxDrugsForPlot = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#33aafd')
        # self.listboxDrugsForPlot.place(x=10, y=164)
        # self.listboxDrugsForPlot.config()

        self.prev_button = Button(text=u"Построить график", background='#d8e1e1',command=self.Draw)
        self.prev_button.place(x=440, y=32)
        self.prev_button.config()

        mainmenu = Menu(root)
        root.config(menu=mainmenu)
        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Открыть БД",command=self.openDB)
        filemenu.add_command(label="Создать новую БД",command=self.createNewDB)
        filemenu.add_command(label="Удалить БД")
        filemenu.add_command(label="Добавить запись в БД",command=self.insertData)
        filemenu.add_command(label="Выход")

        helpmenu = Menu(mainmenu, tearoff=0)
        helpmenu.add_command(label="Помощь")
        helpmenu.add_command(label="О программе")

        mainmenu.add_cascade(label="Файл",
                             menu=filemenu)
        mainmenu.add_cascade(label="Справка",
                             menu=helpmenu)


        self.idx = 0
        self.idxDate = 0
        self.idxDrugs = 0

        self.drugs = []#np.ravel(self.selectFromExpAndMetaExp("DrugName","Drugs"))
        self.name = []#np.ravel(self.selectAllFromTable("Experiments","Name"))


        #self.background(self.print_numbers(10))
        self.selectedRatsByDrugs = range(len(self.name))

        self.g_i()
        self.selectName()
        self.g_i_Drugs()
        self.root.configure(background='#fdfbfb')
        # self.root.mainloop()

    def insertData(self):
        self.newWindow = Tk()
        self.app = InsertWindow(self.newWindow)
        return

    def createNewDB(self):
        dbPath = filedialog.askdirectory()
        if dbPath != "":
            print(dbPath)
            dbName = simpledialog.askstring("Сохранить базу данных", "Введите имя новой базы данных",
                                            parent=self.root)
            self.utils = self.initPresenter.createNewDatabase(dbPath, dbName)
            self.drugs = self.initPresenter.getDrugs()
            self.name = self.initPresenter.getName()
            self.g_i()
            self.selectName()
            self.g_i_Drugs()
        return

    def openDB(self):
        dbPath = filedialog.askopenfilename(filetypes =[('Data Base File', '*.db')])
        if dbPath != "":

            self.utils = Utils(dbPath)
            self.drugs = self.initPresenter.getDrugs(self.utils)
            self.name = self.initPresenter.getName(self.utils)
            self.g_i()
            self.selectName()
            self.g_i_Drugs()
            # self.w = Worker(self.utils)
            # self.w.start()

    def selectName(self, *args):
        value_name = [self.listboxName.get(idx) for idx in self.listboxName.curselection()]

        value_idx = [idx for idx in self.listboxName.curselection()]

        if len(value_name) == 0:
            self.listboxName.select_set(0)
            value_name = [self.listboxName.get(0)]
            value_idx = [0]
        self.idx = value_idx
        self.valueNameAfterClick=value_name
        return value_name, value_idx

    def g_i(self, nameSelectedByDrugs=None):
        if nameSelectedByDrugs!=None:
            name = np.concatenate(nameSelectedByDrugs)
            #print(np.concatenate(name))
        else:
            name=self.name
        self.listboxName.delete(0, 'end')

        itemList = np.array(name)
        for item in itemList:
            self.listboxName.insert(END, item)
        #if nameSelectedByDrugs == None:
        self.listboxName.bind('<<ListboxSelect>>', self.selectName)

        if nameSelectedByDrugs == None:
            self.listboxName.select_set(0)

        else:
            print (self.valueNameAfterClick,self.idx)

            for i in self.idx:
                self.listboxName.select_set(i)
        self.listboxName.event_generate("<<ListboxSelect>>")


    def selectDrugs(self, *args):
        self.selectedRatsByDrugs = []
        value_name = [self.listboxDrugs.get(idx) for idx in self.listboxDrugs.curselection()]
        value_idx = [idx for idx in self.listboxDrugs.curselection()]
        if len(value_name) == 0:
            self.listboxDrugs.select_set(0)
            value_name = [self.listboxDrugs.get(0)]
            value_idx = [0]
        self.selectedDrugs = value_name
        self.idxDrugs = value_idx

        ratNames = self.utils.selectExpByDrugs(drugsFields=self.drugs[self.idxDrugs])

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

    def plotBoundary(self,boundary,cmap):
        self.colorMapRange=[]
        if len(boundary[0])>1:
            for i,color,colorNum in zip(boundary,cmap,range(len(cmap))):
                print (i,'i')
                if i[0]=="Файл не найден":
                    pass
                if i[0] != "Файл не найден" and i[0]!='0':
                    Rostral = float(i[0])
                    print (Rostral)
                    Caudal = float(i[1])
                    Medial = float(i[2])
                    Lateral = float(i[3])
                    self.axes.scatter(Caudal,Medial,color='green')
                    self.axes.scatter(Rostral,Medial,color='green')
                    self.axes.scatter(Caudal,Lateral,color='green')
                    self.axes.scatter(Rostral,Lateral,color='green')
                    xCR = np.linspace(Caudal,Rostral,num=5)
                    yCR = [Medial]*5
                    xCL = [Caudal]*5
                    yCL = np.linspace(Medial,Lateral,num=5)
                    xLR = np.linspace(Caudal,Rostral,num=5)
                    yLR = [Lateral]*5
                    xRL = [Rostral]*5
                    yRL = np.linspace(Medial,Lateral,num=5)
                    self.axes.plot(xCR,yCR,color=color)
                    self.axes.plot(xCL,yCL,color=color)
                    self.axes.plot(xLR,yLR,color=color)
                    self.axes.plot(xRL,yRL,color=color)
                    self.colorMapRange.append(colorNum)

    def plotCord(self,cords,cmap,drugName,cmapDrugs):
        expIds = np.array(cords)[:,-1]
        expId = np.unique(expIds)
        cords = np.array(cords)[:,:2]
        lineForLegend = []
        scatterForLeg = []
        labelForDrug = []
        print (self.colorMapRange)
        for name,color in zip(range(len(self.valueNameAfterClick)),cmap):
            line1 = self.axes.scatter(cords[:,0][expIds==expId[name]],cords[:,1][expIds==expId[name]],facecolors='none',
                              edgecolors=color,linewidth=2,s=75)
            lineForLegend.append(line1)
        lineForLegend=np.array(lineForLegend)[self.colorMapRange]
        for dN,color in zip(self.selectedDrugs,cmapDrugs):
            s1 = self.axes.scatter(cords[:, 0][drugName==dN], cords[:, 1][drugName==dN],
                              facecolors=color,marker='+')
            if len(cords[:, 0][drugName == dN])!=0:
                scatterForLeg.append(s1)
                labelForDrug.append(dN)
        self.fig.legend(lineForLegend, np.array(self.valueNameAfterClick)[self.colorMapRange])
        self.fig.legend(scatterForLeg, labelForDrug,loc='upper left')


    def show(self):
        plt.show()

    def Draw(self):

        self.fig, self.axes = plt.subplots(1, 1, figsize=(10, 10), dpi=100)

        plPresenter = PlotPresenter(self.utils)
        boundary = plPresenter.getBoundary(self.valueNameAfterClick)

        evenly_spaced_interval = np.linspace(0, 1,len(self.valueNameAfterClick)+1)
        evenly_spaced_interval_d = np.linspace(0, 1, len(self.selectedDrugs))
        colors = [cm.rainbow(x) for x in evenly_spaced_interval]
        colorsDrugs = [cm.Paired(x) for x in evenly_spaced_interval_d]

        self.plotBoundary(boundary,colors)

        cords, drugsName = plPresenter.getCords(self.selectedDrugs)
        self.plotCord(cords,colors,drugsName,colorsDrugs)
        self.show()

        return

    def print_numbers(self,end):  # no capitals for functions in python
        for i in range(end):
            print(i)
            time.sleep(1)

    def background(self,func):
        th = threading.Thread(target=func)
        th.start()

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


class Worker(threading.Thread,ObserverPresenter,mainWindow):
    def __init__(self,utils=None):
        super(Worker, self).__init__()
        self.utils = utils

    def run(self):
        while True:
            print ("ack th")
            #self.show()
            # ObserverPresenter.getPath(utils=self.utils)
            # time.sleep(600)

#A = app()
def main():
    root = Tk()
    app = mainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()