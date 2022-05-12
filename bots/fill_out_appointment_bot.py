import random
from typing import Any
from time import sleep

from selenium.webdriver.common.by import By

from bots.person_example import *
from bots.bot_managing import Bot
from bots.bot_mixins import FormFillerMixin, LoginMixin


class FillOutAppointmentBot(Bot, FormFillerMixin, LoginMixin):
    """Filling Appointment Data Bot"""

    def __init__(self, 
                email: str, password: str, 
                person: dict, use_proxy: bool = False) -> None:
        super().__init__(use_proxy)
        self.email = email
        self.password = password
        self.person = person

    def work(self) -> Any:
        self.login(self.email, self.password)
        sleep(2)

        # Start New Booking button
        self.driver.find_element(By.XPATH, "//section/div/div[2]/button/span").click()
        sleep(2)

        self.choose_visa_centre(self.person["VISA_CENTRE"])

        self.choose_visa_category()
        
        self.choose_visa_subcategory()
        
        # Submitt btn for categories
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(4)
        self.driver.find_element(
                            By.XPATH, 
                            "//section/form/mat-card/button/span"
                            ).click()
        sleep(5)
        # Next steps of new booking
        self.fill_person_data_out(self.person)
        sleep(10)
        self.select_appointment_book(self.person)
        sleep(5)
        self.book_review()
        sleep(10)
        self.fill_bank_data_out(self.person)

    def generate_report(self) -> Any:
        return super().generate_report()