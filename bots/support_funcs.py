from datetime import datetime
import json
import subprocess
import polling

import requests

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from .bot_token import CHAT_ID, TOKEN
from .bot_configurations import load_conf, bot_config_parser_on
from .bot_managing import Bot
from bots.exceptions import FireWallException


CONFIG_PARSE = bot_config_parser_on()
DJANGO_CONF = "DJANGO"

CURRENT_HOST = load_conf(CONFIG_PARSE, DJANGO_CONF, "DJANGO_HOST")

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

def send_request_to_get_all_applicants_data_endpoint() -> dict:
    url = CURRENT_HOST + f'api/get-applicants-data/'
    r = requests.get(url)

    return return_data(response=r)

def return_visa_centre():
    data = send_request_to_get_all_applicants_data_endpoint()
    data.append(["END", "END", 0])
    return data

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
            "SUBCATEGORY": data['subcategory']
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

def send_request_to_start_filler_bot_endpoint(
    visa_centre: str, subcategory: str, free_windows: list,
    month: str):
    message = f"""
    Visa center: {visa_centre}\n
    Subcategory: {subcategory}\n
    Free dates for appointment: {free_windows}\n
    Month: {month}\n
    """
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}'

    response = requests.get(url)
    return return_data(response)

def is_firewall_blocked_at_the_end(func):
    def wrapper(*args, **kwargs):
        driver = args[0].driver
        func_result = func(*args, **kwargs)
        messages = """
                    Sorry, we've been unable to progress with your request right now. 
                    Please try again in one hour on a single device, after you have closed all your browser windows, 
                    disconnected from a VPN and cleared your cache memory.
                   """
        path_of_url = 'page-not-found'

        if driver.title == messages or path_of_url in driver.current_url:
            raise FireWallException("Firewall blocked selenium!")
        return func_result

    return wrapper

def is_firewall_blocked_at_the_start(func):
    def wrapper(*args, **kwargs):
        driver = args[0].driver
        messages = """
                    Sorry, we've been unable to progress with your request right now. 
                    Please try again in one hour on a single device, after you have closed all your browser windows, 
                    disconnected from a VPN and cleared your cache memory.
                   """
        path_of_url = 'page-not-found'

        if driver.title == messages or path_of_url in driver.current_url:
            raise FireWallException("Firewall blocked selenium!")
        return func(*args, **kwargs)

    return wrapper

def intialize_bot_with_firewall_bypass(bot_class: Bot, **optional):
    try:
        bot = bot_class(**optional)
        bot.work()
    except (FireWallException, ElementClickInterceptedException):
        bot.driver.quit()
        del bot
        print("Firewall blocked selenium\nTrying to recreate driver...")
        intialize_bot_with_firewall_bypass(bot_class, **optional)

def find_element_with_retry_base(driver, element_locator, by, refresh):
    wait_time = 20
    retries = 1
    while retries <= 3:
        try:
            return WebDriverWait(
                driver, wait_time).until(
                    ec.presence_of_element_located((by, element_locator)))
        except TimeoutException:
            wait_time += 5
            retries += 1
            refresh and driver.refresh()
        except ElementClickInterceptedException:
            wait_time += 5
            retries += 1
        except StaleElementReferenceException:
            wait_time += 5
            retries += 1


def find_element_with_retry_by_id(driver, element_id, refresh=False):
    return find_element_with_retry_base(driver, element_id, By.ID, refresh)


def find_element_with_retry_by_class(driver, element_class, refresh=False):
    return find_element_with_retry_base(driver, element_class, By.CLASS_NAME, refresh)


def find_element_with_retry_by_xpath(driver, element_xpath, refresh=False):
    return find_element_with_retry_base(driver, element_xpath, By.XPATH, refresh)