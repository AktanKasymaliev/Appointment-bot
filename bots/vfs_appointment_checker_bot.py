from typing import Any
from time import sleep

from selenium.webdriver.common.by import By

from bots.bot_managing import Bot
from bots.bot_mixins import FormFillerMixin, LoginMixin
from bots.support_funcs import  return_visa_centre


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
            # return 'All visa centres viewed'
            self.current_visa_index  = 0 
            self.current_visa = self.VISA_CENTRES_AND_SUBCATEGORIES[self.current_visa_index]

    def __get_current_centre(self) -> str:
        return self.current_visa[0]

    def __get_current_subcategory(self) -> str:
        return self.current_visa[1]

    def __check_appointment_time(self):
        #Continue button
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base"
        )
        sleep(5)
        #TODO Add checking logic. We need 1.day; 2.How many hours are available
        pass

    def work(self) -> Any:
        self.login(self.email, self.password)
        sleep(2)
        # Start New Booking button
        self.driver.find_element(By.XPATH, "//section/div/div[2]/button/span").click()
        sleep(2)
        self.check()

    def check(self):
        current_visa_centre = self.__get_current_centre()
        current_subcategory = self.__get_current_subcategory()
        if current_visa_centre[0] == "END":
            self.driver.quit()
            return

        self.choose_visa_centre(current_visa_centre)

        self.choose_visa_category()
        
        self.choose_visa_subcategory(current_subcategory)
        sleep(3)

        message = self.driver.find_element(By.XPATH, "//div[4]/div").text
        if message in self.NO_APPOINTMENT:
            self.__next_visa()
            self.check()

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