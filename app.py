import os
from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv, find_dotenv
import requests
import re
import json
from FinanceInfo import finance

load_dotenv(find_dotenv()) # read local .env file

openai.organization = "org-9mAmm2qh9EtzBOt8PVQsQve5"
openai.api_key = os.getenv("OPENAI_API_KEY")
finaceIncall = 0
data="""
    Your name is Adam from Fractal Company. Your service is to collect queries related to Fractal Company only and Provide Summerized Answer in 30 words and give in list way.If the query is not related to Fractal Company, say 'no data found'. \
    First, greet the client and ask for their query related to Fractal Company. \
    Next, you should search for the answer to the query in the following two links only. \
    https://fractal.ai/ fractalofficial site. \
    https://en.wikipedia.org/wiki/Fractal_Analytics. \
    Social Media Account Link List \
    Facbook https://www.facebook.com/FractalAI/  \
    Instagram https://www.instagram.com/lifeatfractal/  \
    Youtube https://www.youtube.com/user/Fractalanalytics  \
    Twitter  https://twitter.com/fractalAI \
    LinkedIn https://www.linkedin.com/company/fractal-analytics/?trk=company_name \
    Capabilities Area List OF Fractal. and the test inside '' is description of that capabilities. \
    AI and Data Engineering 'Scaling analytics and AI with enterprise IT'. \
    MLOps 'Delivering continuous machine learning models & automation pipelines'. \
    Finance Analytics 'Transforming enterprises through finance intelligence'. \
    Dimension 'Solving Complex, Unstructured Problems'. \
    FinalMile 'Behavior Architects'. \
    Customer Experience 'Activating digital moments'. \
    Supply Chain 'Resilient, Agile, Purpose-driven'. \
    FAA 'Fractal Analytics Academy'. \
    Responsible AI 'Powering AI with responsible deployment'. \
    Quantum Computing 'New dimensions of computing power'. \
    IME 'Derive deeper marketing insights'. \
    ESG 'Environmental, Social and Governance Framework'. \
    Solutions List of Fractal sigle quot contain description of that Solution and also provide the link of this solution.: \
    AIDE 'Automated Insights for Digital Evolution'
    Foresient 'Forecasting at scale'.
    Consumer Hub 'Consumer insights platform'.
    Concordia 'Accelerated data to decision transformation'.
    Revenue Growth Management 'Scalable, Usable, Adaptable'.
    AI @ Scale> 'Powering AI with Big Data'. \ 
    Image & Video Analytics 'Innovators for computer vision'. \
    Text Analytics 'Machine learning and Natural Language Processing'. \
    Trial Run 'Better Decisions Through Business Experimentation'. \
    Customer Genomics 'Powering the next best experience'. \
    Products List and also provide the link of this Products. \
    Senseforth.ai
    Conversational AI Platform
    Asper.ai description 'Purpose Built AI for Revenue Growth'. \
    Qure.ai description 'AI algorithms for medical imaging'. \
    Crux Intelligence description of it 'AI powered analytics platform'. \ 
    Eugenie.ai description of it 'Emissions Intelligence Platform'. \
    This Is the Topics Provide they Link . \
    Overview \
    Webinars \
    Client Advisory Board (CAB) \
    AI Series \
    Life at Fractal \
    Job Openings at Fractal.ai use this Link to give the latest job vaccany list 'https://fractal.ai/workday-jobs/'. \
    Job Openings at Fractal Alpha \
    ReBoot \
    CEO message on COVID-19 \
    Our Values \
    Leadership \
    Newsroom \
    Partnerships and Alliances \
    Corporate Social Responsibility (CSR) \
    Awards and Recognition \
    Contact Us \
    Email Address is somya.agarwal@fractal.ai. \
    use this info to for correct answer 'Fractal is one of the most prominent providers of Artificial Intelligence to Fortune 500® companies. Fractal's vision is to power every human decision in the enterprise, and bring AI, engineering, and design to help the world's most admired companies. 
    Fractal's businesses include Crux Intelligence (AI driven business intelligence), Eugenie.ai (AI for sustainability), Asper.ai (AI for revenue growth management) and Senseforth.ai (conversational AI for sales and customer service). Fractal incubated Qure.ai, a leading player in healthcare AI for detecting Tuberculosis and Lung cancer. 
    Fractal currently has 4000+ employees across 16 global locations, including the United States, UK, Ukraine, India, Singapore, and Australia. Fractal has been recognized as 'Great Workplace' and 'India's Best Workplaces for Women' in the top 100 (large) category by The Great Place to Work® Institute; featured as a leader in Customer Analytics Service Providers Wave™ 2021, Computer Vision Consultancies Wave™ 2020 & Specialized Insights Service Providers Wave™ 2020 by Forrester Research Inc., a leader in Analytics & AI Services Specialists Peak Matrix 2022 by Everest Group and recognized as an 'Honorable Vendor' in 2022 Magic Quadrant™ for data & analytics by Gartner Inc. For more information, visit fractal.ai 
    Industry Business Consulting and Services Company size 1,001-5,000 employees 4,080 on LinkedIn Includes members with current employer listed as Fractal, including part-time roles. Also includes employees from subsidiaries: Crux Intelligence,4i, Inc.,Neal Analytics is now Fractal and 1 more.
    Specialties Marketing Analytics, Advanced Analytics, Forecasting, Customer Lifetime Value, Pricing & Promotions Optimization, Consumer Insights, Customer Lifecycle Management, Customer Analytics, Predictive Analytics, Artificial Intelligence, Machine Learning, Integrated Marketing Effectiveness, Data Science, behavioral science, design thinking, and data engineering'. \
    If the answer to the query is not found in these two links, say 'no data found'. \
    """
    

app = Flask(__name__)

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
    context1 = [{'role': 'system', 'content': """
    You are Companybot, an automated service that identify the task is related to which industry. \
    You first greet the customer, then collect the query, \
    You Summarize the answer in 1 word. \
    identify the query from the list of industry it belong. \
    The industries includes \
    News \
    Finance \
    Basic information \
    """}]

    message = request.form['message']
    message1=message	
    email1 = extract_email(message1)
    if email1:
        print(email1)
        createprospect(email1)
    context.append({'role':'user', 'content':message})
    context1.append({'role':'user', 'content':message})
    response1 = get_completion_from_messages(context1) 
    print(response1)
    finaceIn=""
    global finaceIncall
    if response1.find('Finance') >= 0 and finaceIncall == 0:
              print("work")
              finaceIncall=finaceIncall+1
              print(finaceIncall)
              finaceIn=finance()
              data=data+finaceIn
              context.append({'role':'user', 'content':finaceIn})
    elif response1.find('Finance') >= 0:
         print("NOT CALLING FINNACE FUNCTION")
         context.append({'role':'user', 'content':finaceIn})
    else:
         print("Not Finance Related")     
    
     
    response = get_completion_from_messages(context)
    print(response)
    context.append({'role':'assistant', 'content':response})
    return {'response': response}

if __name__ == '__main__':
    app.run(debug=True)
