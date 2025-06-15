from PIL import Image
from PIL import ImageGrab
import io
import time
import pyperclip
import easyocr
import hashlib
import os
from multiprocessing import Process,Queue,cpu_count
import multiprocessing
from typing import Optional
import numpy
import shutil
import keyboard
multiprocessing.set_start_method('spawn',force=True)

class ImageOCR:

    
    
    

    def __init__(self):
        self.image_queue = Queue(maxsize=100)
        self.result_queue = Queue(maxsize=100)
        self.p_num = 0
        self.runing = False
        self.processes = []
        self.questions = []
        os.makedirs("textfile",exist_ok=True)
        keyboard.add_hotkey("ctrl+shift+r",self.revocate)
        
    def ready(self):
        print("ready")

    def hash_text(self,text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def hash_image(self,image):
        return hashlib.md5(image.tobytes()).hexdigest()

    def abstract_text_from_image(self,image):
        
        image_np = numpy.array(image)
        result = self.reader.readtext(image_np)
        text = ''.join([t for (_, t , _) in result])

        return text

    def save_image(self,image,num):
        filename = f"p_{num}"
        image.save("textfile\\"+filename+".png","PNG")
        print("number: ",num," save as "+"textfile\\"+filename)

    def delete_image(self,num):
        filename = f"p_{num}"
        if os.path.exists("textfile\\"+filename+".png"):
            os.remove("textfile\\"+filename+".png")
            print("number: ",num," delete "+"textfile\\"+filename)
        else:
            print("file dont exist")

    def revocate(self):
        if self.questions:
            r_question = self.questions.pop()
            self.p_num = self.p_num-1
            print(f"delete question: {r_question}")
            self.delete_image(self.p_num+1)
        else:
            print("cant delete empty question")


    def worker_process(self):
        print("worker_process is runing")
        self.reader = easyocr.Reader(['ch_sim','en'],gpu=True)
        print("reader initialized")
        self.ready()
        while True:
            try:
               
                task = self.image_queue.get(timeout=1)
                if task is None:
                    print("picture analysis stop")
                    self.result_queue.put(None)
                    break
                image,number = task
                try:
                    self.save_image(image,number)
                    print("processing ",number)
                    result = self.abstract_text_from_image(image)
                    print("processed ",number)
                    
                    self.result_queue.put(result)
                    
                    

                except Exception as e:
                    print(f"e1:{e}")
                    
            except self.image_queue.Empty:
                time.sleep(0.3)
                continue
                    
    def start(self):
        print('starting....')
        self.p = Process(target=self.worker_process)
        self.p.start()
        self.clipboard_monitor()
        return self.questions

    def end(self):
        self.image_queue.put(None)
        print("stop monitor")

        while self.p.is_alive():
            time.sleep(0.5)
            print("waiting attach process")
        print("attach process ended")
        shutil.rmtree("textfile//")
                
        print("ocr is ended successfully ",len(self.questions)," questions were recoreded")

    def clipboard_monitor(self):
        last_hash = None
        current_hash = None
        next_num = 1
        pyperclip.copy('')
        print("monitor started")
        
        while True:
            # print(last_hash)
            if self.result_queue.empty()==0:
                q = self.result_queue.get()
                self.questions.append(q)
                print(f"question {len(self.questions)} {q}was captured")
            try:
                image = ImageGrab.grabclipboard()
                if image is not None:
                    current_hash = self.hash_image(image)
                    # print(current_hash)
                    if current_hash != last_hash:
                        last_hash = current_hash
                        self.p_num = self.p_num+1
                        

                        if not self.image_queue.full():
                            self.image_queue.put((image.copy(),self.p_num))
                            print(self.p_num,"added,queue: ",self.image_queue.qsize())
                        else:
                            print("warning : queue is full")

                else:
                    text = pyperclip.paste()
                    if text == '':
                        time.sleep(0.5)
                        continue
                    current_hash = self.hash_text(text)
                    if current_hash != last_hash and current_hash != "":
                        last_hash = current_hash
                        print(f"update {text}")
                time.sleep(0.5)
            except KeyboardInterrupt:
                if self.result_queue.empty()==0:
                    continue
                self.end()
                
                break
            except Exception as e:
                print(f"{e}")
                time.sleep(0.5)
        return self.questions

