from typing import Any
from time import sleep

from selenium.webdriver.common.by import By

from bots.bot_managing import Bot

from bots.bot_mixins import FormFillerMixin
from bots.bot_mixins import LoginMixin
from bots.constants import HEAVY_TIMEOUT
from bots.constants import LIGHT_TIMEOUT
from bots.constants import MEDIUM_TIMEOUT
from bots.support_funcs import  is_firewall_blocked_at_the_end
from bots.support_funcs import  is_firewall_blocked_at_the_start
from bots.support_funcs import  find_element_with_retry_by_xpath
from bots.support_funcs import  return_visa_centre
from bots.support_funcs import  send_request_to_start_filler_bot_endpoint


class VFSAppointmentCheckerBot(Bot, FormFillerMixin, LoginMixin):
    """Checking available appointments date for users"""

    FAKE_PERSON = {
            "FIRST_NAME": "Joe",
            "LAST_NAME": "Baidenn",
            "GENDER": "Male",
            "DATE_OF_BIRTH": "05061997",
            "CITIZIENSHIP": "Kyrgyzstan",
            "PASSPORT_NUMBER": '123123123123',
            "Passport_Expirty_Date": '20082030',
            "PHONE_CODE": '123',
            "PHONE_NUMBER": '123123123',
            "EMAIL":'gmail@gmail.com',
        }

    NO_APPOINTMENT = (
        "No appointment slots are currently available",
        "Currently No slots are available for selected category, please confirm waitlist\nTerms and Conditions"
            )

    def __init__(self, email: str, password: str, use_proxy: bool = False) -> None:
        super().__init__(use_proxy)
        self.email = email
        self.password = password

        self.VISA_CENTRES_AND_SUBCATEGORIES = return_visa_centre()

        self.current_visa_index = 0
        self.current_visa = self.VISA_CENTRES_AND_SUBCATEGORIES[self.current_visa_index]
    
    def __next_visa(self) -> str or None:
        if (len(self.VISA_CENTRES_AND_SUBCATEGORIES) - 1) > self.current_visa_index:
            self.current_visa_index += 1
            self.current_visa = self.VISA_CENTRES_AND_SUBCATEGORIES[self.current_visa_index]
        else:

            self.current_visa_index  = 0 
            self.current_visa = self.VISA_CENTRES_AND_SUBCATEGORIES[self.current_visa_index]

    def __get_current_centre(self) -> str:
        return self.current_visa[0]

    def __get_current_subcategory(self) -> str:
        return self.current_visa[1]

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def __check_appointment_time(self):
        #Continue button
        self.driver.find_element(
            By.XPATH,
            "//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base']/span"
            ).click()
        sleep(MEDIUM_TIMEOUT)

        month = self.driver.find_element(By.CLASS_NAME, 'fc-toolbar-title').text

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(MEDIUM_TIMEOUT)

        a_tags_with_windows = self.driver.find_elements(
            By.XPATH,
            "//td[contains(@class,'date-availiable')]//a[@class='fc-daygrid-day-number']"
        )

        # Pagination in months
        # self.driver.find_element(
        #     By.XPATH,
        #     "//button[@class='fc-next-button fc-button fc-button-primary']/span"
        # ).click()

        free_windows = [int(date.text) for date in a_tags_with_windows]

        send_request_to_start_filler_bot_endpoint(
            visa_centre=self.__get_current_centre(),
            subcategory=self.__get_current_subcategory(),
            free_windows=free_windows,
            month=month
        )
        sleep(1000)

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def work(self) -> Any:
        print('Started to work. Trying to login.')
        self.login(self.email, self.password)
        print('Logged in. Trying to select visa center, category and subcategory.')
        self.check()

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def check(self):
        current_visa_centre = self.__get_current_centre()
        print(f'Working with {current_visa_centre} visa center.')
        current_subcategory = self.__get_current_subcategory()
        if current_visa_centre[0] == "END":
            print("No applicants! Closing.")
            self.driver.quit()
            return
        self.choose_visa_centre(current_visa_centre)
        self.choose_visa_category()
        self.choose_visa_subcategory(current_subcategory)
        sleep(LIGHT_TIMEOUT)

        message = self.driver.find_element(By.XPATH, "//div[4]/div").text
        if message in self.NO_APPOINTMENT:
            print('There are no appointment slots for this visa center. Trying to go with the next one.')
            self.__next_visa()
            print('Set the next visa center. No checking again.')
            self.check()

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(LIGHT_TIMEOUT)
        print('Trying to submit on categories.')
        self.click_submit_on_categories()
        print('Trying to fill out the person form.')
        self.fill_person_data_out(self.FAKE_PERSON)
        sleep(HEAVY_TIMEOUT)
        print('Trying to check appointment time.')
        self.__check_appointment_time()
        sleep(1000)

    def generate_report(self) -> Any:
        return super().generate_report()