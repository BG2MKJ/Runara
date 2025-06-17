import tkinter as tk
from ocr import ImageOCR
from chat import Chat_Api

class UI:
    def confirm_button_click():
        pass


    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Runara")
        self.label_info = tk.Label(self.root,text="Runara")
        self.root.geometry("500x500")
        self.label_info.pack()
        self.question_text = tk.Text(self.root)
        self.question_text.place(x=10,y=50,width=480,height=380)
        self.confirm_button = tk.Button(self.root,text="confirm",command=self.confirm_button_click)
        self.confirm_button.place(x=220,y=440,width=80,height=30)


        self.root.mainloop()


u = UI()