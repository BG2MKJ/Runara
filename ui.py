import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import version as v
from multiprocessing import Process,Queue,cpu_count
import multiprocessing
import queue
import configparser
from typing import Any, Optional
from ocr import ImageOCR
from chat import Chat_Api
class Config:
    def set_config(self,section:str,item:str,value:Any):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config[section][item]=str(value)
        self.save_config()

    def read_config(self,section:str,item:str,fallback=None)->Any:
        return self.config.get(section,item,fallback=fallback)
    
    def save_config(self,config_file="config.ini")->Any:
        with open(config_file,'w') as f:
            self.config.write(f)

    def __init__(self,config_file = "config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        




class UI:
    def get_input(self,title:str="input",prompt:str="input"):
        
        input_str = simpledialog.askstring(title,prompt,parent=self.root)
        if input_str is None:
            return None
        print(input_str)
        return input_str

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

    def load_config(self):
        self.api_key=self.config.read_config("API","apikey")
        print("load apikey",self.api_key)

    def set_key(self):
        self.api_key=self.get_input("input apikey","input apikey")
        if self.api_key is not None:
            self.config.set_config("API","apikey",self.api_key)
            print("set apikey",self.api_key)

    def show_key(self):
        messagebox.showinfo("apikey",self.api_key)

    def set_infolabel(self,text):
        self.info_label.config(text=str(text))

    def ui_set(self):
        
        self.root.title("Runara")
        self.root.geometry("500x500")
        self.root.resizable(False,False)

        self.meunbar=tk.Menu(self.root)
        self.filemeun = tk.Menu(self.meunbar,tearoff=0)
        self.filemeun.add_command(label="设置key",command=self.set_key)
        self.filemeun.add_command(label="查看key",command=self.show_key)
        self.meunbar.add_cascade(label="文件",menu=self.filemeun)

        self.helpmeun = tk.Menu(self.meunbar,tearoff=0)
        self.meunbar.add_cascade(label="帮助",menu=self.helpmeun)
        


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

        self.info_label = tk.Label(self.root,text="init",font="华文新魏 12")
        self.info_label.place(x=320,y=16)

    def start_queue_checking(self):
        if not self.running:
            return
        try:
            data = self.data_queue.get_nowait()
            print("queue:",data)
            if data[0]=="info":
                self.info_label.config(text=data[1])
            if data[0]=="question":
                self.question_text.delete("1.0",tk.END)
                self.question_text.insert("1.0","\n\n".join(data[1]))
        except queue.Empty:
            pass
        finally:
            
            self.root.after(100,self.start_queue_checking)

    def ui_start(self):
        self.root.mainloop()
        self.running = 0
        self.back.terminate()

    def __init__(self,ocr_class,data_queue:Queue):
        self.running = 1
        self.api_key=""
        self.root = tk.Tk()
        self.data_queue = data_queue

        self.config=Config()
        self.load_config()
        # self.ocr_process = Process(target=ocr.start)
        # self.ocr_process
        self.start_queue_checking()
        self.back = Process(target=ocr_class(data_queue).start)
        self.back.start()
        self.ui_set()
        self.ui_start()
        


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)
    dataqueue = Queue()
    

    u = UI(ImageOCR,dataqueue)

