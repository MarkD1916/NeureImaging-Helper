class Rat():
    def __init__(self):
        self.mass: int = 0
        self.drags: list[str] = [""]
        self.coudBound: int = 0
        self.medBoud: int = 0
        self.latBound: int = 0
        self.rostBound: int = 0
        self.coords: list[[int,int]] = [[0,0]]
        self.folderName: str = " "
        self.date: str = " "
        self.name:str = " "

class Date():
    def __init__(self):
        self.date = ""
        self.ratName = ""


class Drugs():
    def __init__(self):
        self.name: str = ""


class Concentration():
    def __init__(self):
        pass

