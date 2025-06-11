from openai import OpenAI
import requests
import json

class Chat_Api:
    api_key = ''
    client =  OpenAI(api_key=api_key,base_url="https://api.deepseek.com")
    def __init__(self,set_api_key):
        self.api_key = set_api_key
        self.client.api_key=set_api_key
    
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

chat_api = Chat_Api("sk-4dd7b73b63a149518ffd105c7a464634")
print(chat_api.request_balance())
