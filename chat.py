from openai import OpenAI
import requests
from multiprocessing import Queue
import json

class Chat_Api:
    api_key = ''
    client =  OpenAI(api_key=api_key,base_url="https://api.deepseek.com")


    def __init__(self,set_api_key,data_queue:Queue):
        self.api_key = set_api_key
        self.client.api_key=set_api_key
        self.data_queue = data_queue

    def set_ley(self,key:str):
        self.api_key = key

    def send_data(self,head:str,data):
        send = (head,data)
        self.data_queue.put(send)

    def generate_promots(self,num_of_questions):
        promots = f"接下来我将给你{num_of_questions}道题目，帮我解答，注意B选项可能错误识别为8。你只需要告诉我答案不需要写解析，你要快速输出。"+"输出格式：题干+换行+答案标号和答案内容+换行+解释+换行+换行"
        return promots

    def format_output(self,answer):
        j_answer = json.loads(answer)
        format_output = []
        for e in j_answer:
            format_output.append([e["question"],e["type"],e["options"],e["answer"],e["explanation"]])
        return format_output
    
    def chat_to_ai(self,question):
        messages = [{"role": "user", "content": question}]
        response = self.client.chat.completions.create(model="deepseek-reasoner",messages=messages)
        content = response.choices[0].message.content
        return content
    
    def request_balance(self):
        print("asking")
        url = "https://api.deepseek.com/user/balance"
        payload={}
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + self.api_key
        }
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            response_json = json.loads(response.text)
            balance = (response_json["balance_infos"][0]["total_balance"])
        except Exception as e:
            print(e)
            return None
        self.send_data("balance",balance)
        return balance

    def ask_question(self,questions:str):
        text_question = self.generate_promots(len(questions))
        for q in questions:
            text_question+=q
        print("requesting...")
        answers = self.chat_to_ai(text_question)

        return answers
    
    def print_single_answer(self,format_output):
        for e in format_output:
            print(e[0],e[1],e[3])
    
