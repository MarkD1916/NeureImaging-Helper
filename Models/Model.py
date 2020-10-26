class Session():
    def __init__(self):
        self.sessionID:int = 0
        self.RatID: int = 0
        self.drags: list[str] = [""]
        self.coudBound: int = 0
        self.medBoud: int = 0
        self.latBound: int = 0
        self.rostBound: int = 0
        self.coords: list[[int,int]] = [[0,0]]
        self.folderName: str = " "
        self.date: str = " "


class Rat():
    def __init__(self):
        self.RatID:int = 0
        self.mass: int = 0
        self.name: str = " "

