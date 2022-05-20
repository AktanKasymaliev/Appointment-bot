from datetime import datetime
import json
import subprocess
import polling

import requests

CURRENT_HOST = "http://localhost:8000/"

def start_create_applicant_account_bot(applicant_id: int):
    subprocess.Popen(
        ['python', 
        'manage.py', 
        'run_account_creator_command', 
        f'--applicant_id={applicant_id}'
        ]
    )

def send_request_to_aws_lambda(): pass


def return_data(response) -> dict:
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return f"Something went wrong with {response.status_code} code"

def send_request_to_add_email_password_endpoint(applicant_id: int, email: str, password: str) -> dict or str:
    url = CURRENT_HOST + f'api/create-applicant-account/{applicant_id}/'

    r = requests.patch(
        url,
        data={
                "email": email,
                "email_password": password
            }
        )
    
    return return_data(response=r)


def send_request_to_get_applicant_data_endpoint(applicant_id: int) -> dict or str:
    url = CURRENT_HOST + f'api/get-applicant-data/{applicant_id}/'
    r = requests.get(url)

    return return_data(response=r)

def make_person_for_bot(applicant_id: int, email: str, card_data: dict) -> dict:
    data = send_request_to_get_applicant_data_endpoint(applicant_id)

    card_valid_through = datetime.strptime(card_data['valid_through'], '%Y-%m-%d')
    date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
    passport_expiry_date = datetime.strptime(data['passport_expiry_date'], '%Y-%m-%d')

    return {
            #personality
            "FIRST_NAME": data['firstname'],
            "LAST_NAME": data['lastname'],
            "GENDER": data['gender'].title(),
            "DATE_OF_BIRTH": date_of_birth.strftime('%d%m%Y'),
            "CITIZIENSHIP": data['citizenship'],
            "PASSPORT_NUMBER": data['passport'],
            "Passport_Expirty_Date": passport_expiry_date.strftime('%d%m%Y'),
            "PHONE_CODE": data['phone_code'],
            "PHONE_NUMBER": data['contact_number'],
            "EMAIL": email,

            #card info
            "cart_num": card_data['number'],
            "expiry_month": card_valid_through.strftime('%m'),
            "expiry_year": card_valid_through.strftime('%Y'),
            "cvv": card_data['code'],
            "name_and_surname": "Joe Baidenn",
            "address": "Pushkin\'s street...)",
            "city_district_postcode": "Moscow, Lublino disctrict, 000000",
            
            #free appointment window
            "FREE_WINDOW": 30,
            "VISA_CENTRE": data['visa_centre'],
        }

def test_status_code(response):
    return response.status_code == 200

def get_card() -> dict:
    url = CURRENT_HOST + 'api/get-first-free-card/'
    response = polling.poll(
        lambda: requests.get(url),
        step=60,
        poll_forever=True,
        check_success=test_status_code
    )
    return json.loads(response.text)    