import os
from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv, find_dotenv
import requests
import re
import json
from bardapi import Bard

load_dotenv(find_dotenv()) # read local .env file

openai.organization = "org-9mAmm2qh9EtzBOt8PVQsQve5"
apiKey="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"
openai.api_key = apiKey
finaceIncall = 0
NewsIncall = 0
BasicIncall = 0
data = """
    Your name is Adam from Fractal Company. Your service is to collect queries related to Fractal Company only. \
    Your task is to Summarized the answer in 30 Words. \
    Include astrick marked content. \
    Provide the Answer In Formet Of List. \
    If the query is not related to Fractal Company, say 'no data found'. \
     """
    


app = Flask(__name__)

def get_answer(Query):
        os.environ['_BARD_API_KEY'] = 'Wwjy9enUyqj-vt-QYzH6diFnKyCxOoAELeYflLz9xFyKAFcNyAx--v-UIEct509xyX6OPw.'
        session = requests.Session()
        session.headers = {
                    "Host": "bard.google.com",
                    "X-Same-Domain": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "Origin": "https://bard.google.com",
                    "Referer": "https://bard.google.com/",
                }
        session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 
        bard = Bard(token=os.getenv("_BARD_API_KEY"), session=session, timeout=30)
        ans=bard.get_answer(Query)['content']
        print('bard Answer ', ans)
        return ans

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def extract_email(string):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return None

def gettoken():
    url = "https://login.salesforce.com/services/oauth2/token"
    payload = {
     'client_id': '3MVG9fe4g9fhX0E4rB1MeKF0UTUC0MIyoSgh1s93CRKKtf0Jqt2Tu7087Isfn2kAFc._.530IW.XtK3lowSxk',
     'client_secret': 'BA2470D1D4FF3761AA981A03773AC01547A5E7CBA35B116247702F858902B302',
     'username': 'dipanshu@aethereus.com',
     'password': '112001Dip#@kay6opTZTXbwtnwgepw0mJoyi',
     'grant_type': 'password'
           }
    files=[
          ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    access_token = response.json().get("access_token")
    instance_url = response.json().get("instance_url")
    print("Access Token:", access_token)
    print("Instance URL", instance_url)
    return access_token
    

def createprospect(email1):
    print(email1)
    api = gettoken()
    print(api)
    url = "https://pi.demo.pardot.com/api/v5/objects/prospects?fields=email"
    payload = json.dumps({"email": email1})
    headers = {
     'Pardot-Business-Unit-Id': '0Uv5g0000008OQUCA2',
     'Content-Type': 'application/json',
     'Authorization': 'Bearer '+api,
     'Cookie': 'pardot=48csbc6a7e6olpppml1kmjbgj2'
    }
    response = requests.request("POST", url, headers=headers, data=payload) 
    print(response.text)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global data
    context = [ {'role':'system', 'content':data} ]# accumulate messages
    
    message = request.form['message']
    message1=message	
    email1 = extract_email(message1)
    if email1:
        print(email1)
        createprospect(email1)
    
    response1 = get_answer(message) 
    print(response1)

    context.append({'role':'user', 'content':response1}) 
    response = get_completion_from_messages(context)
    print('Chat gpt answer ', response)
    context.append({'role':'assistant', 'content':response})
    return {'response': response}

if __name__ == '__main__':
    app.run(debug=True)
