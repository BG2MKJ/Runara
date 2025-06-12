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
multiprocessing.set_start_method('spawn',force=True)

class ImageOCR:

    
    
    

    def __init__(self):
        self.image_queue = Queue(maxsize=100)
        self.p_num = 0
        self.runing = False
        self.processes = []
        self.questions = []
        os.makedirs("textfile",exist_ok=True)
        

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

    def worker_process(self):
        print("worker_process is runing")
        self.reader = easyocr.Reader(['ch_sim','en'],gpu=True)
        print("reader initialized")
        while True:
            try:
                task = self.image_queue.get(timeout=1)
                if task is None:
                    print("picture analysis stop")
                    break
                image,number = task
                try:
                    self.save_image(image,number)
                    
                    result = self.abstract_text_from_image(image)
                    self.questions.append(result)

                    print(self.questions)

                except Exception as e:
                    print(f"e1:{e}")
                    
            except:
                continue
                    
    def start(self):
        print('starting....')
        p = Process(target=self.worker_process)
        p.start()
        self.clipboard_monitor()

    def clipboard_monitor(self):
        last_hash = None
        current_hash = None
        next_num = 1
        pyperclip.copy('')
        print("monitor started")
        
        while True:
            # print(last_hash)
            try:
                image = ImageGrab.grabclipboard()
                if image is not None:
                    current_hash = self.hash_image(image)
                    if current_hash != last_hash:
                        last_hash = current_hash
                        self.p_num = self.p_num+1
                        

                        if not self.image_queue.full():
                            self.image_queue.put((image.copy(),self.p_num))
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
                
                self.image_queue.put(None)
                print("stop monitor")
                shutil.rmtree("textfile//")
                break
            except Exception as e:
                print(f"{e}")
                time.sleep(0.5)



if __name__ == '__main__':
    # 所有执行代码放在这里
    imageocr = ImageOCR()
    # text = imageocr.abstract_text_from_image("textfile\\t2.png")
    # print(text)

    imageocr.start()