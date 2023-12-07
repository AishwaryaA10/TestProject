import pandas as pd
import requests
import json

#client_id = os.environ['client_id']

def login():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    login_data = {"grant_type": "password",
                  "client_id": "mosaic-gatekeeper",
                  "client_secret": "fee2aaac-454b-463d-b5e1-94b1da4d1fc8",
                  "username": "ravikumar",
                  "password": "098f6bcd4621d373cade4e832627b4f6"
                  }
    request_url = "https://refract-login.fosfor.com/auth/realms/mosaic/protocol/openid-connect/token"
    data = requests.post(request_url, data=login_data, headers=headers)
    # print(data.json())
    token = data.json().get("access_token")
    return token


Access_token = login();

print(Access_token)

inp1={
"payload":
{"sk_id_curr":1009870,
 "amt_credit": 526491.0,
 "amt_goods_price":454500.0,
 "credit_agency_1_rating":0.0,
 "credit_agency_2_rating":0.0396256,
 "credit_agency_3_rating":0.231439,
 "days_credit": -898.667,
 "days_credit_enddate": -332.5,
 "remaining_installment":5.45455,
 "buro_avg_amt_instalment": 21946.1,
 "buro_max_amt_instalment": 39770.5,
 "occupation_type": 'Laborers',
 "organization_type": 'Industry: type 11',
 "code_gender": 'M',
 "days_birth": 16347,
 "days_id_publish": 3450,
 "customer_since": 6238,
 "annual_income": 520000,
 "days_employed": 922,
 "name_contract_type": 'Cash loans',
 "target":  0
}
}


# @st.experimental_memo
def application_scorecard(payload):
    Access_token = login()
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + Access_token}
    url = "https://refract.fosfor.com/applicationscorecard/7b529978-19fc-47e2-a512-b126688f287e/score"
    #data = {"payload": payload}
    #inp_data = json.dumps(data)
    inp_payload = json.dumps(payload)
    response_json = requests.post(url, data=inp_payload, headers=headers)

    # st.text_input("API Response: ",response_json.content)
    response = response_json.json()
    try:
        print("success")
        print(response['data'])
        return response['data']
    except ValueError:
        print("failure")
        return response_json.status_code

application_scorecard(inp1)

