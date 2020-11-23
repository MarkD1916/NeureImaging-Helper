class Experiments():
    def __init__(self,ID,path, method):
        self.ID: int = ID
        self.path:str = path
        self.method:str = method


class Rat():
    def __init__(self,ID,expID,name,mass):
        self.ID:int = ID
        self.mass: int = mass
        self.name: str = name
        self.expID = expID


class Boundary():
    def __init__(self,ID,rostral,caudal,medial,lateral,expID):
        self.rostral:float = rostral
        self.caudal:float = caudal
        self.medial:float = medial
        self.lateral:float = lateral
        self.expID: int = expID
        self.ID: int = ID

class Drugs():
    def __init__(self,expID,drugName,valve,ID):
        self.expID:int = expID
        self.drugName:str = drugName
        self.valve:int = valve
        self.ID: int = ID

class Cords():
    def __init__(self,expID,ID,xValue,yValue,region):
        self.expID=expID
        self.ID=ID
        self.xValue=xValue
        self.yValue=yValue
        self.region=region

