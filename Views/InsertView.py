from tkinter import *
from tkinter import filedialog,simpledialog
from Presenters.Presenter import InsertPresenter
class InsertWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("Добавление записи в БД")
        self.root.geometry("660x300")
        self.frame = Frame(self.root)
        self.frame.place()

        text = Text(self.root)
        vsb = Scrollbar(self.root,orient="vertical", command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")


        height = 4
        width = 20
        for i in range(height):  # Rows
            text.place(x=i * 10, y=1)
            for j in range(width):
                b = Entry(self.root, text="")

                #b.place(x=30 + i * 150, y=30 + j * 40)
                text.window_create("end", window=b)
                text.insert("end", "\n")

        text.configure(state="disabled")