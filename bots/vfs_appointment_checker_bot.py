from typing import Any
from time import sleep

from selenium.webdriver.common.by import By

from person_example import *
from bots.bot_managing import Bot
from bots.bot_mixins import FormFillerMixin, LoginMixin


class VFSAppointmentCheckerBot(Bot, FormFillerMixin, LoginMixin):
    """Checking available appointments date for users"""

    FAKE_PERSON = {
            "FIRST_NAME": "Joe",
            "LAST_NAME": "Baidenn",
            "GENDER": "Male",
            "DATE_OF_BIRTH": "05061997",
            "CITIZIENSHIP": "Kyrgyzstan",
            "PASSPORT_NUMBER": '20506200414356',
            "Passport_Expirty_Date": '20082030',
            "PHONE_CODE": '996',
            "PHONE_NUMBER": '0559055934',
            "EMAIL":'gmail@gmail.com',
        }


    VISA_CENTRES = (
        "Poland Visa Application Center - Ankara",
        "Poland Visa Application Center-Antalya",
        "Poland Visa Application Center-Beyoglu",
        "Poland Visa Application Center-Gaziantep",
        "Poland Visa Application Center-Izmir",
        "Poland Visa Application Center-Trabzon"
    )

    NO_APPOINTMENT = (
        "No appointment slots are currently available",
        "Currently No slots are available for selected category, please confirm waitlist\nTerms and Conditions"
            )

    def __init__(self, email: str, password: str,  use_proxy: bool = False) -> None:
        super().__init__(use_proxy)
        self.email = email
        self.password = password

        self.current_visa_index = 0
        self.current_visa = self.VISA_CENTRES[self.current_visa_index]
    
    def __next_visa(self) -> str or None:
        if (len(self.VISA_CENTRES) - 1) > self.current_visa_index:
            self.current_visa_index += 1
            self.current_visa = self.VISA_CENTRES[self.current_visa_index]
        else:
            self.current_visa_index  = 0 
            self.current_visa = self.VISA_CENTRES[self.current_visa_index]

    def __get_current_centre(self) -> str:
        return self.current_visa

    def __check_appointment_time(self):
        #TODO Add checking logic. We need 1.day; 2.How many hours are available
        pass

    def work(self) -> Any:
        self.login(self.email, self.password)
        sleep(2)

        # Start New Booking button
        self.driver.find_element(By.XPATH, "//section/div/div[2]/button/span").click()
        sleep(2)

        self.choose_visa_centre(self.__get_current_centre())

        self.choose_visa_category()
        
        self.choose_visa_subcategory()
        sleep(3)

        message = self.driver.find_element(By.XPATH, "//div[4]/div").text
        if message in self.NO_APPOINTMENT:
            self.__next_visa()
            self.work() 
            #TODO add 'if operator' if the list of visa centres ends, it will stop checking

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(4)
        self.driver.find_element(
                            By.XPATH, 
                            "//section/form/mat-card/button/span"
                            ).click()
        sleep(5)
        self.fill_person_data_out(self.FAKE_PERSON)
        sleep(5)
        self.__check_appointment_time()
        sleep(1000)

    def generate_report(self) -> Any:
        return super().generate_report()