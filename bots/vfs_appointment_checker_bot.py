import random
from typing import Any
from time import sleep

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from person_example import *
from bots.bot_managing import Bot


class FillOutAppointmentBot(Bot):
    """Еще не доделано нужно дописать стабильную логику """
    
    URL = "https://visa.vfsglobal.com/tur/en/pol/login"
    VISA_CENTRES = (
        "Poland Visa Application Center - Ankara",
        "Poland Visa Application Center-Antalya",
        "Poland Visa Application Center-Beyoglu",
        "Poland Visa Application Center-Gaziantep",
        "Poland Visa Application Center-Izmir",
        "Poland Visa Application Center-Trabzon"
    )
    VISA_CATEGORY = "National Visa (Type D) / Uzun Donem  / Wiza typu D"
    VISA_SUBCATEGORY = "2- Work permit / Calisma Izni / w celu wykonywania pracy"

    NO_APPOINTMENT = (
        "No appointment slots are currently available",
        "Currently No slots are available for selected category, please confirm waitlist\nTerms and Conditions"
            )

    def __init__(self, email: str, password: str,  use_proxy: bool = False) -> None:
        self.driver = self.create_driver(use_proxy)
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

    def login(self) -> None:
        self.driver.get(self.URL)
        sleep(15)
        try:
            self.driver.find_element(By.ID, 'mat-input-0').send_keys(self.email)
            sleep(2)
            self.driver.find_element(By.ID, 'mat-input-1').send_keys(self.password)
            sleep(2)
            self.driver.find_element(By.CLASS_NAME, 'mat-btn-lg').click()
            sleep(15)
            self.driver.find_element(By.ID, 'onetrust-close-btn-container').click()
            # Start New Booking button
            self.driver.find_element(By.XPATH, "//section/div/div[2]/button/span").click()
            sleep(2)
        except:
            print("Email or password was given incorrect!")

    def __click_button(self, class_name: str) -> None:
        self.driver.find_element(
            By.XPATH, "//button[@class='{}']/span".format(class_name)
            ).click()
    
    def __mat_select(self, arg: str) -> None:
        try:
            self.driver.find_element(By.XPATH,
                "//mat-option/span[contains(text(), '{}')]".format(arg)
            ).click()
        except NoSuchElementException:
            raise Exception("Visa centre not found: {}".format(arg))

    def __choose_visa_centre(self, visa_center) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//mat-form-field/div/div/div[3]"
        ).click()
        sleep(6)

        self.__mat_select(visa_center)
        sleep(5)

    def __choose_visa_category(self) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//div[@id='mat-select-value-3']"
        ).click()
        sleep(6)
        
        self.__mat_select("Schengen Visa  (Type C) / Kisa Donem / Wiza typu C")
        sleep(5)

    def __choose_visa_subcategory(self) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//div[@id='mat-select-value-5']"
        ).click()
        sleep(6)
        self.__mat_select("4- Short-Stay others / Diger Kisa Donem / wiza typu C w celu innym niz wymienione")
        sleep(5)

    def __fill_person_data_out(self) -> None:
        #First name
        self.driver.find_element(By.ID, 'mat-input-2').send_keys(FIRST_NAME)
        sleep(2)
        #Last name
        self.driver.find_element(By.ID, 'mat-input-3').send_keys(LAST_NAME)
        sleep(2)
        # Gender
        self.driver.find_element(
            By.XPATH,
            "//div[@id='mat-select-value-7']".format()
             ).click()
        sleep(2)
        self.__mat_select(GENDER)
        sleep(2)
        #Date of Birth
        self.driver.find_element(By.ID, 'dateOfBirth').send_keys(DATE_OF_BIRTH)
        sleep(2)
        #Citizienship
        self.driver.find_element(
            By.XPATH, "//div[@id='mat-select-value-9']"
            ).click()
        sleep(2)
        self.__mat_select(CITIZIENSHIP)
        sleep(2)
        #Passport number
        self.driver.find_element(By.ID, 'mat-input-4').send_keys(PASSPORT_NUMBER)
        sleep(2)
        #Passport Expirty Date
        self.driver.find_element(By.ID, 'passportExpirtyDate').send_keys(Passport_Expirty_Date)
        sleep(2)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(2)
        # Phonenumber code without '+'
        self.driver.find_element(By.ID, 'mat-input-5').send_keys(PHONE_CODE)
        sleep(2)
        # Phone number
        self.driver.find_element(By.ID, 'mat-input-6').send_keys(PHONE_NUMBER)
        sleep(2)
        # Email
        self.driver.find_element(By.ID, 'mat-input-7').send_keys(EMAIL)
        sleep(5)
        # Save button
        self.__click_button(
            "mat-focus-indicator mat-stroked-button mat-button-base btn btn-block btn-brand-orange mat-btn-lg"
        )
        sleep(10)
        self.__select_appointment_book()
        sleep(100)
    
    def __select_appointment_book(self):
        #Continue button
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base"
        )
        sleep(2)
        #Book Appointment section filling out
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(5)
        self.driver.find_element(
            By.XPATH,
            '//a[text()={}]'.format(FREE_WINDOW_DAY)
            ).click()
        sleep(3)
        try:
            self.__click_button(
                "mat-focus-indicator btn mat-btn-lg btn-block load-more mat-stroked-button mat-button-base mat-button-disabled ng-star-inserted"
            )
        except ElementNotInteractableException:
            pass
        sleep(3)
        appointment_hours = self.driver.find_elements(
            By.XPATH,
            "//div[@class='ba-slot-box ng-star-inserted']"
            )
        sleep(3)
        random.choice(appointment_hours).click()
        sleep(4)
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base"
        )
        sleep(5)
        self.__book_review()

    def work(self) -> Any:
        self.__choose_visa_centre(self.__get_current_centre())

        self.__choose_visa_category()
        
        self.__choose_visa_subcategory()
        sleep(3)

        message = self.driver.find_element(By.XPATH, "//div[4]/div").text
        if message in self.NO_APPOINTMENT:
            self.__next_visa()
            self.work()

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(4)
        self.driver.find_element(
                            By.XPATH, 
                            "//section/form/mat-card/button/span"
                            ).click()
        sleep(5)
        self.__fill_person_data_out()

    def generate_report(self) -> Any:
        return super().generate_report()