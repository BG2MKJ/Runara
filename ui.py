import tkinter as tk
import version as v
# from ocr import ImageOCR
# from chat import Chat_Api

class UI:
    def confirm_button_click(self):
        pass

    def confirm_button_click(self):
        pass

    def revocate_button_click(self):
        pass

    def set_question_count(self,n):
        self.questions_count_label.config(text=str(n))
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Runara")
        self.label_info = tk.Label(self.root,text="Runara",font="华文新魏 20")
        
        self.root.geometry("500x500")
        self.label_info.pack()
        self.question_text = tk.Text(self.root)
        self.question_text.place(x=10,y=50,width=480,height=380)
        self.confirm_button = tk.Button(self.root,text="Confirm",command=self.confirm_button_click)
        self.confirm_button.place(x=120,y=440,width=80,height=30)
        self.revocate_button = tk.Button(self.root,text="Revocate",command=self.revocate_button_click)
        self.revocate_button.place(x=320,y=440,width=80,height=30)
        self.questions_count_label = tk.Label(self.root,text="0",font="华文新魏 15")
        self.questions_count_label.place(x=20,y=440,height=40,width=40)
        self.set_question_count(343)

        self.root.mainloop()


u = UI()