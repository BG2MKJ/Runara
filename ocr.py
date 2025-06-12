from PIL import Image
from PIL import ImageGrab
import io
import time
import pyperclip
import easyocr
import hashlib

class ImageOCR:

    p_num = 0

    def hash_text(self,text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def hash_image(self,image):
        return hashlib.md5(image.tobytes()).hexdigest()

    def abstract_text_from_image(self,image_path):
        reader = easyocr.Reader(['ch_sim','en'])
        img = Image.open(image_path)
        result = reader.readtext(image_path)
        text = ''.join([t for (_, t , _) in result])

        return text

    def save_image(self,image,num):
        filename = f"p_{num}"
        image.save("textfile\\"+filename+".png","PNG")
        print("number: ",num," save as "+"textfile\\"+filename)

    def clipboard_monitor(self):
        last_hash = None
        current_hash = None
        next_num = 1
        pyperclip.copy('')
        print("start monitor")
        
        while True:
            # print(last_hash)
            try:
                image = ImageGrab.grabclipboard()
                if image is not None:
                    current_hash = self.hash_image(image)
                    if current_hash != last_hash:
                        last_hash = current_hash
                        self.p_num = self.p_num+1
                        self.save_image(image,self.p_num)
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
                print("stop monitor")
                break
            except Exception as e:
                print(f"{e}")
                time.sleep(0.5)

imageocr = ImageOCR()
# text = imageocr.abstract_text_from_image("textfile\\t2.png")
# print(text)

imageocr.clipboard_monitor()