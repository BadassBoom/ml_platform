import json

import requests

API_URL = "https://dq9xj08l24.execute-api.eu-north-1.amazonaws.com/default"

upload_data = {
    "action": "upload",
    "csv_data": "year,odometer,engine_power,accident_status,price_usd\n2016,243000,1.8,1,11000\n2007,190000,2.97,0,11500\n2011,166000,2.0,0,9599\n2012,138000,1.8,0,10499\n2007,280000,4.66,0,12200"
}

upload_response = requests.post(API_URL, data=json.dumps(upload_data))  
print("Upload Response:", upload_response.json())

predict_data = {
    "action": "predict",
    "input_data": [2012, 140000, 2.0, 0]
}

predict_response = requests.post(API_URL, data=json.dumps(predict_data))
print("Prediction Response:", predict_response.json())

update_data = {
    "action": "update",
    "csv_data": "2015,130000,2.5,1,8000"
}

update_response = requests.post(API_URL, data=json.dumps(update_data))
print("Update Response:", update_response.json())
