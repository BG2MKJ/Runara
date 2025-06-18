import tkinter as tk
import version as v
import configparser
from typing import Any, Optional
# from ocr import ImageOCR
# from chat import Chat_Api
class Config:
    def set_config(self,config:configparser.ConfigParser,item:str):
        pass

    def read_config(self,config:configparser.ConfigParser,item:str):
        return config.get(str)


    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.read_config()




class UI:
    def confirm_button_click(self):
        pass

    def confirm_button_click(self):
        pass

    def revocate_button_click(self):
        pass

    def set_question_count(self,n):
        self.questions_count_label.config(text=str(n))

    def set_balance(self,n):
        self.balance.config(text=str(n))

    def set_text(self,text):
        pass

    def set_key(self):
        pass

    
        

    def __init__(self):

        self.api_key=""

        self.root = tk.Tk()
        self.root.title("Runara")
        self.root.geometry("500x500")
        self.root.resizable(False,False)

        self.meunbar=tk.Menu(self.root)
        self.filemeun = tk.Menu(self.meunbar,tearoff=0)
        self.filemeun.add_command(label="设置key",command=self.set_key)
        self.meunbar.add_cascade(label="文件",menu=self.filemeun)

        self.root.config(menu=self.meunbar)

        self.label_info = tk.Label(self.root,text="Runara",font="华文新魏 20")
        self.label_info.pack()

        self.question_text = tk.Text(self.root,font="华文新魏 14")
        self.question_text.place(x=10,y=50,width=460,height=380)

        self.question_text_scrollbar = tk.Scrollbar(self.root)
        self.question_text_scrollbar.place(x=470, y=50, height=380) 

        self.question_text.config(yscrollcommand=self.question_text_scrollbar.set)
        self.question_text_scrollbar.config(command=self.question_text.yview)
        
        self.confirm_button = tk.Button(self.root,text="Confirm",command=self.confirm_button_click)
        self.confirm_button.place(x=220,y=440,width=80,height=30)

        self.revocate_button = tk.Button(self.root,text="Revocate",command=self.revocate_button_click)
        self.revocate_button.place(x=320,y=440,width=80,height=30)

        self.questions_count_label = tk.Label(self.root,text="0",font="华文新魏 15")
        self.questions_count_label.place(x=120,y=440,height=40,width=40)
        
        self.balance = tk.Label(self.root,text="0.45",font="华文新魏 15")
        self.balance.place(x=120,y=10,height=40,width=40)

        self.yourbalance_label = tk.Label(self.root,text="Your balance:",font="华文新魏 12")
        self.yourbalance_label.place(x=10,y=16)

        self.questioncount_label = tk.Label(self.root,text="Questions count:",font="华文新魏 12")
        self.questioncount_label.place(x=10,y=446)



        self.root.mainloop()


u = UI()