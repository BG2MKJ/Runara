from openai import OpenAI
import requests
import json

class Chat_Api:
    api_key = ''
    client =  OpenAI(api_key=api_key,base_url="https://api.deepseek.com")


    def __init__(self,set_api_key):
        self.api_key = set_api_key
        self.client.api_key=set_api_key
    
    def generate_promots(self,num_of_questions):
        promots = f"接下来我将给你{num_of_questions}道题目，帮我解答，注意B选项可能错误识别为8。:"
        return promots


    def chat_to_ai(self,question):
        messages = [{"role": "user", "content": question}]
        response = self.client.chat.completions.create(model="deepseek-reasoner",messages=messages)
        content = response.choices[0].message.content
        return content
    
    def request_balance(self):
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
        return balance

    def ask_question(self,questions):
        text_question = self.generate_promots(len(questions))
        for q in questions:
            text_question+=q
        print("requesting...")
        answers = self.chat_to_ai(text_question)
        return answers
        
        

