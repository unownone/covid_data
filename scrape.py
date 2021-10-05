import requests
import bs4
import re
from tqdm import tqdm
from flask import current_app as app
from flask_pymongo import PyMongo
from datetime import datetime,timedelta

mongo = PyMongo(app)
covid_data = mongo.db.covid_data.data

EXP_HR = 5
EXP_DAY = 0
EXP_MIN = 0


def main_function():
    search = covid_data.find_one({'dataname':'covidData'})
    if search is not None:
        if search['created_at']<datetime.now():
            data = getCovidData()
            data['created_at'] = datetime.now()+timedelta(minutes = EXP_MIN,hours = EXP_HR,days = EXP_DAY)
            covid_data.update_one({'dataname':'covidData'},data)
            return data
        else:
            del search['_id']
            return search
    else:
        data = getCovidData()
        data['dataname']='covidData'
        data['created_at'] = datetime.now()+timedelta(minutes = EXP_MIN,hours = EXP_HR,days = EXP_DAY)
        covid_data.insert_one(data)
        return data


def snake_case(name):
    name = re.sub(r'([^a-zA-Z/ ])', r'', name.strip())
    return re.sub(r'[ /]+', r'_', name).lower()

def clean_data(text):
    text = re.sub(r'(\t|\n| |\r|\xa0)+', r' ', text).upper()
    return text.strip()

def getCovidData():
    link ='https://www.worldometers.info/coronavirus/'

    resp = requests.get(link)

    soup = bs4.BeautifulSoup(resp.text,'html.parser')

    table = soup.find('table',{'id':'main_table_countries_today'})
    headers = table.find_all('th')
    data = table.find_all('td')
    covid = {}
    for i in range(0,len(data),len(headers)):
        partial = {}
        for j in range(2,len(headers)):
            partial[snake_case(headers[j].text)] = clean_data(data[i+j].text)
        covid[snake_case(data[i+1].text)] = partial
    covid['dataname'] = 'covidData'
    return covid



import time

curr = time.time()
main_function()
print("Time taken: ", round((time.time()-curr),3),'seconds')