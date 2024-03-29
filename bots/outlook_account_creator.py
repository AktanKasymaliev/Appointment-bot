import os
import random
import secrets
import string
from time import sleep
from pprint import pprint

from faker import Faker

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from anycaptcha import AnycaptchaClient, FunCaptchaProxylessTask

from bots.bot_managing import Bot

API_2_CAPTCHA = os.environ.get("ANYCAPTCHA_KEY")


class OutlookAccountCreator(Bot):
    """ Class for creating outlook.com account
        with randomly generated details  """

    URL = 'https://signup.live.com/signup'
    SURL = 'https://client-api.arkoselabs.com'

    def work(self):
        """
        Goes through website process of creating the account
        :return: dictionary with login information for the account
        """
        self.driver.get(self.URL)
        sleep(2)
        self.driver.find_element(By.ID, 'liveSwitch').click()
        sleep(2)

        person = self.__generate_random_details()
        birth_date = person['dob']

        try:
            # Enter Email
            ActionChains(self.driver) \
                .send_keys_to_element(self.driver.find_element(By.ID, 'MemberName'), person['username']) \
                .send_keys(Keys.ENTER).pause(3).perform()
            # Enter Password
            ActionChains(self.driver) \
                .send_keys_to_element(self.driver.find_element(By.ID, 'PasswordInput'), person['password']) \
                .send_keys(Keys.ENTER).pause(4).perform()
            # Enter First and Last Name
            ActionChains(self.driver) \
                .send_keys_to_element(self.driver.find_element(By.ID, 'FirstName'), person['first_name']) \
                .send_keys_to_element(self.driver.find_element(By.ID, 'LastName'), person['last_name']) \
                .send_keys(Keys.ENTER).pause(3).perform()

            # Enter Country and DOB
            self.driver.find_element(By.XPATH, f'//option[@value="{person["country"]}"]').click()
            WebDriverWait(self.driver, 1
                                ).until(
                                    EC.element_to_be_clickable((By.XPATH, '//*[@id="BirthYear"]'))
                                    ).send_keys(birth_date.year)
            sleep(1)

            birthD = Select(self.driver.find_element(By.ID, "BirthDay"))
            birthD.select_by_visible_text(str(birth_date.day))
            sleep(1)

            month_select = self.driver.find_element(By.XPATH, '//*[@id="BirthMonth"]')
            month_select.find_element(By.XPATH, f'//*[@value="{birth_date.month}"]').click()
            sleep(1)

            self.driver.find_element(By.ID, 'iSignupAction').click()
            sleep(5)

            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@id="enforcementFrame"]')))
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@id="fc-iframe-wrap"]')))
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@id="CaptchaFrame"]')))
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "home_children_button"))).click()
            sleep(3)
        except:
            print('Failed while creating account...\nRetrying...')
            return self.work()

        # Solve Captcha
        self.driver.switch_to.default_content()
        src = self.driver.find_element(By.ID, "enforcementFrame").get_attribute('src')
        pk = [i for i in src.split('/') if i.startswith("B7D")][-1]
        solution = self.__solve_captcha(pk)

        js_script = f"""
                    var anyCaptchaToken = '{solution}';
                    var enc = document.getElementById('enforcementFrame');
                    var encWin = enc.contentWindow || enc;
                    var encDoc = enc.contentDocument || encWin.document;
                    let script = encDoc.createElement('SCRIPT');
                    script.append('function AnyCaptchaSubmit(token) {{ parent.postMessage(JSON.stringify({{ eventId: "challenge-complete", payload: {{ sessionToken: token }} }}), "*") }}');
                    encDoc.documentElement.appendChild(script);
                    encWin.AnyCaptchaSubmit(anyCaptchaToken);
                    """

        self.driver.execute_script(js_script)

        sleep(10)

        report = self.generate_report(person)
        if report != None:
            self.driver.close()
            print('=========Mail created!=========')
            return report

        print('Failed to create account...')
        return None
    
    def generate_report(self, person: dict) -> dict or None:
        if 'account.microsoft' in self.driver.current_url:
            email = person['username'] + '@outlook.com'
            print(f'Account created successfully ({email})...')
            person['dob'] = person['dob'].strftime('%d, %b %Y')
            person['email'] = email
            pprint(person, indent=4)
            return person
        return None


    @staticmethod
    def __generate_random_details():
        """
        Generates random details for new account
        :return: dictionary with fake details
        """
        fake_details = Faker()
        name = fake_details.name()
        username = OutlookAccountCreator.__create_username(name)
        password = OutlookAccountCreator.__generate_password()
        first, last = name.split(' ', 1)

        while True:
            dob = fake_details.date_time()
            if dob.year < 2000:
                break
            if dob.month != 2:
                break
        while True:
            country = fake_details.country_code(representation="alpha-2")
            if country != "GB":
                break
        return {
            "first_name": first,
            'last_name': last,
            'country': country,
            'username': username,
            'password': password,
            'dob': dob
        }

    @staticmethod
    def __create_username(name: str):
        """
        Creates username based on name
        :param name: string with person name
        :return: string with username based on the name
        """
        return name.replace(' ', '').lower() + str(random.randint(100, 100000))

    @staticmethod
    def __generate_password() -> str:
        """
        generates password 10 char long, with at least one number and symbol
        :return: string with new password
        """
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(9))
        return password + random.choice('$#@!') + random.choice('0123456789') + random.choice('QWERTYUIOPLKJH')

    def __solve_captcha(self, pk: str) -> str:
        """
        downloads captcha image and send to 2captcha to solve
        :param pk: Site key of url
        :return: token(str) with captcha solution
        """
        try:
            print('Solving Captcha...')
            client = AnycaptchaClient(API_2_CAPTCHA)
            solver = FunCaptchaProxylessTask(
                website_url=self.driver.current_url,
                website_key=pk
                )
            
            job = client.createTask(solver, typecaptcha="funcaptcha")
            job.join()
            solution = job.get_solution_response()

            print(f"Captcha solved!")
            return solution

        except Exception as e:
            print('Failed to solve captcha...\nRetrying to solve')
            sleep(5.5)
            return self.__solve_captcha(pk)