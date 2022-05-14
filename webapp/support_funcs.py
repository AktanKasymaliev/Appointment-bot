import subprocess

import requests
from django.http import JsonResponse

from config.settings import CURRENT_HOST

def start_create_applicant_account_bot(applicant_id: int):
    subprocess.Popen(
        ['python', 
        'manage.py', 
        'run_account_creator_command', 
        f'--applicant_id={applicant_id}'
        ]
    )

def send_request_to_aws_lambda() -> tuple: pass


def send_request_to_endpoint(applicant_id: int, email: str, password: str) -> JsonResponse or str:
    url = CURRENT_HOST + f'api/create/applicant/account/{applicant_id}/'

    r = requests.patch(
        url,
        data={
                "email": email,
                "email_password": password
            }
        )
    if r.status_code == 200:
        return r.content
    else:
        return f"Something went wrong with {r.status_code} code"

def make_person_for_bot(applicant: object, email: str) -> dict:
    return {
            #personality
            "FIRST_NAME": applicant.firstname,
            "LAST_NAME": applicant.lastname,
            "GENDER": applicant.gender.title(),
            "DATE_OF_BIRTH": applicant.date_of_birth.strftime('%d%m%Y'),
            "CITIZIENSHIP": applicant.citizenship,
            "PASSPORT_NUMBER": applicant.passport,
            "Passport_Expirty_Date": applicant.passport_expiry_date.strftime('%d%m%Y'),
            "PHONE_CODE": applicant.phone_code,
            "PHONE_NUMBER": applicant.phone_number,
            "EMAIL": email,

            #card info
            "cart_num": '4123123123123',
            "expiry_month": 1,
            "expiry_year": 24,
            "cvv": 111,
            "name_and_surname": "Joe Baidenn",
            "address": "Pushkin\'s street...)",
            "city_district_postcode": "Moscow, Lublino disctrict, 000000",
            
            #free appointment window
            "FREE_WINDOW": 30,
            "VISA_CENTRE": "Poland Visa Application Centre - Ankara",
        }