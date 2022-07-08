from typing import Any
from time import sleep

from bots.bot_managing import Bot
from bots.bot_mixins import FormFillerMixin, LoginMixin
from bots.support_funcs import is_firewall_blocked_at_the_end, is_firewall_blocked_at_the_start
from bots.constants import HEAVY_TIMEOUT, LIGHT_TIMEOUT, MEDIUM_TIMEOUT

class FillOutAppointmentBot(Bot, FormFillerMixin, LoginMixin):
    """Filling Appointment Data Bot"""

    def __init__(self, 
                email: str, password: str, 
                person: dict, use_proxy: bool = False) -> None:
        super().__init__(use_proxy)
        self.email = email
        self.password = password
        self.person = person

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def work(self) -> Any:
        self.login(self.email, self.password)
        sleep(MEDIUM_TIMEOUT)
        self.choose_visa_centre(self.person["VISA_CENTRE"])

        self.choose_visa_category()
        
        self.choose_visa_subcategory(self.person["SUBCATEGORY"])
        
        # Submit btn for categories
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(LIGHT_TIMEOUT)
        self.click_submit_on_categories()
        # Next steps of new booking
        self.fill_person_data_out(self.person)
        sleep(HEAVY_TIMEOUT)
        self.select_appointment_book(self.person)
        sleep(MEDIUM_TIMEOUT)
        self.book_review()
        sleep(HEAVY_TIMEOUT)
        self.fill_bank_data_out(self.person)

    def generate_report(self) -> Any:
        return super().generate_report()