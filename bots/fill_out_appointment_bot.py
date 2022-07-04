from typing import Any
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bots.bot_managing import Bot
from bots.bot_mixins import FormFillerMixin, LoginMixin
from bots.support_funcs import is_firewall_blocked

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
        if not is_firewall_blocked(self.driver): 
            sleep(7)
            
            # Start New Booking button
            self.driver.find_element(By.XPATH, "//section/div/div[2]/button/span").click()
            sleep(4)

            self.choose_visa_centre(self.person["VISA_CENTRE"])

            self.choose_visa_category()
            
            self.choose_visa_subcategory(self.person["SUBCATEGORY"])
            
            # Submit btn for categories
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(4)
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "//section/form/mat-card/button/span"))
            ).click() 
            sleep(7)
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