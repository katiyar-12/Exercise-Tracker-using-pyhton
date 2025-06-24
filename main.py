from os import environ

import requests
import datetime as dt
import os


# data to be saved in environment variables
 
APP_ID = os.environ["nutrition_api_id"]
API_KEY = os.environ["nutrition_api"]
NUTRITION_API_END_POINT = os.environ["nutrition_api_end_point"]
SHEETY_API_END_POINT = os.environ["sheety_api_end_point"]

# for authentication
sheety_user_name = os.environ.get("sheety_user_name")
sheety_user_password = os.environ.get("sheety_user_password")

def current_time() :
    hour = dt.datetime.now().time().hour
    minutes = int(dt.datetime.now().time().minute)
    seconds = int(dt.datetime.now().time().second)
    seconds = round(seconds,1)

    return f"{hour}-{minutes}-{seconds}"

headers = {
    "x-app-id" : APP_ID ,
    "x-app-key" : API_KEY ,
    'Content-Type': 'application/json' ,
}

parameters = {
    "query" : input("which exercise did you do today : ") ,
}





response = requests.post(url=NUTRITION_API_END_POINT, json=parameters, headers=headers)
response.raise_for_status()
whole_data = response.json()

# working with sheety


duration = str(whole_data["exercises"][0]["duration_min"]) + " min"
calories = str(whole_data["exercises"][0]["nf_calories"])
exercise = whole_data["exercises"][0]["name"]
today = str(dt.datetime.today().date())

sheety_row =  {
    "workout" : {
        "exercise" : exercise ,
        "date" : today ,
        "time" : current_time() ,
        "duration" : duration ,
        "calories" : calories ,
    }
}



sheet_response = requests.post(url=SHEETY_API_END_POINT,json=sheety_row,auth=(sheety_user_name,sheety_user_password))
sheet_response.raise_for_status()
