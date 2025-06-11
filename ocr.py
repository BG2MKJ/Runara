from PIL import Image
import easyocr

def abstract_text_from_image(image_path):
    reader = easyocr.Reader(['ch_sim','en'])
    img = Image.open(image_path)
    result = reader.readtext(image_path)
    text = ''.join([t for (_, t , _) in result])

    return text

text = abstract_text_from_image("textfile\\t2.png")
print(text)