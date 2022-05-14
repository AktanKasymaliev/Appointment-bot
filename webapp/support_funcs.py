from django.http import JsonResponse
import requests

from bots import outlook_account_creator, outlook_account_mail_checker, vfs_account_creator, \
                    mail_login_bot, fill_out_appointment_bot
from config.settings import CURRENT_HOST

def start_create_applicant_account_bot() -> tuple:
    outlook_mail = outlook_account_creator.OutlookAccountCreator(use_proxy=True).work()
    email = outlook_mail['email']
    password = outlook_mail['password']

    mail_login_bot.MailLoginBot(
        email=email,
        password=password,
        use_proxy=True
    ).work()

    vfs_account_creator.VFSAccountCreate(
        email=email,
        password=password,
        use_proxy=True
        ).work()

    outlook_account_mail_checker.OutlookCheckerMailBot(
        email=email,
        password=password,
        use_proxy=True
        ).work()
    
    fill_out_appointment_bot.FillOutAppointmentBot(
        email=email,
        password=password,
        person={"key": "value"},
        use_proxy=True
    ).work()
    
    return email, password

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
        return r.json()
    else:
        return f"Something went wrong with {r.status_code} code"