class Experiments():
    def __init__(self,ID=None,path='', name='', date=''):
        self.ID: int = ID
        self.path:str = path
        self.name:str = name
        self.date: str = date




class Rat():
    def __init__(self,ID,expID,name,mass):
        self.ID:int = ID
        self.mass: int = mass
        self.name: str = name
        self.expID = expID


class Boundary():
    def __init__(self,ID=None,rostral=0,caudal=0,medial=0,lateral=0,expID=0):
        self.ID: int = ID
        self.rostral:float = rostral
        self.caudal:float = caudal
        self.medial:float = medial
        self.lateral:float = lateral
        self.expID: int = expID


class Drugs():
    def __init__(self,expID=0,drugName='',valve=0,ID=None):
        self.ID: int = ID
        self.expID = expID
        self.drugName:str = drugName
        self.valve:int = valve



class Cords():
    def __init__(self,expID=0,ID=None,xValue=0,yValue=0):
        self.ID = ID
        self.xValue=xValue
        self.yValue=yValue
        self.expID = expID
        #self.region=region

class Users():
    def __init__(self):
        pass