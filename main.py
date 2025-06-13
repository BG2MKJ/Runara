
from ocr import ImageOCR
from chat import Chat_Api


def main():

    imageocr = ImageOCR()
    chat_api = Chat_Api("sk-4dd7b73b63a149518ffd105c7a464634")

    
    questions = imageocr.start()
    
    answer=chat_api.ask_question(questions)
    print(answer)
    print(chat_api.request_balance())
    input()


if __name__ == '__main__':
    main()
    