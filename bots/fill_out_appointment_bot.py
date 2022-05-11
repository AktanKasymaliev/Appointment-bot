import random
from typing import Any
from time import sleep

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from bots.person_example import *
from bots.bot_managing import Bot


class FillOutAppointmentBot(Bot):
    
    URL = "https://visa.vfsglobal.com/tur/en/pol/login"

    VISA_CATEGORY = "Schengen Visa  (Type C) / Kisa Donem / Wiza typu C"
    VISA_SUBCATEGORY = "4- Short-Stay others / Diger Kisa Donem / wiza typu C w celu innym niz wymienione"

    def __init__(self, 
    email: str, password: str,  
    visa_centre: str, person: dict,
     use_proxy: bool = False) -> None:
        super().__init__(use_proxy)
        self.email = email
        self.password = password
        self.VISA_CENTRE = visa_centre
        self.person = person

    def login(self) -> None:
        self.driver.get(self.URL)
        sleep(15)
        # Logining attempt
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
        """
        It clicks on the dropdown menu, then clicks on the option that matches the argument
        
        :param arg: The name of the visa centre you want to select
        :type arg: str
        """
        try:
            self.driver.find_element(By.XPATH,
                "//mat-option/span[contains(text(), '{}')]".format(arg)
            ).click()
        except NoSuchElementException:
            raise Exception("Visa centre not found: {}".format(arg))

    def __choose_visa_centre(self) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//mat-form-field/div/div/div[3]"
        ).click()
        sleep(6)

        self.__mat_select(self.VISA_CENTRE)
        sleep(5)

    def __choose_visa_category(self) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//div[@id='mat-select-value-3']"
        ).click()
        sleep(6)
        
        self.__mat_select(self.VISA_CATEGORY)
        sleep(5)

    def __choose_visa_subcategory(self) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//div[@id='mat-select-value-5']"
        ).click()
        sleep(6)
        self.__mat_select(self.VISA_SUBCATEGORY)
        sleep(5)

    def __fill_person_data_out(self) -> None:
        #First name
        self.driver.find_element(By.ID, 'mat-input-2').send_keys(self.person["FIRST_NAME"])
        sleep(2)
        #Last name
        self.driver.find_element(By.ID, 'mat-input-3').send_keys(self.person["LAST_NAME"])
        sleep(2)
        # Gender select
        self.driver.find_element(
            By.XPATH,
            "//div[@id='mat-select-value-7']"
             ).click()
        sleep(2)
        self.__mat_select(self.person["GENDER"])
        sleep(2)
        #Date of Birth
        self.driver.find_element(By.ID, 'dateOfBirth').send_keys(self.person["DATE_OF_BIRTH"])
        sleep(2)
        #Citizienship select
        self.driver.find_element(
            By.XPATH, "//div[@id='mat-select-value-9']"
            ).click()
        sleep(2)
        self.__mat_select(self.person["CITIZIENSHIP"])
        sleep(2)
        #Passport number
        self.driver.find_element(By.ID, 'mat-input-4').send_keys(self.person["PASSPORT_NUMBER"])
        sleep(2)
        #Passport Expirty Date
        self.driver.find_element(By.ID, 'passportExpirtyDate').send_keys(self.person["Passport_Expirty_Date"])
        sleep(2)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(2)
        # Phonenumber code without '+'
        self.driver.find_element(By.ID, 'mat-input-5').send_keys(self.person["PHONE_CODE"])
        sleep(2)
        # Phone number
        self.driver.find_element(By.ID, 'mat-input-6').send_keys(self.person["PHONE_NUMBER"])
        sleep(2)
        # Email
        self.driver.find_element(By.ID, 'mat-input-7').send_keys(self.person["EMAIL"])
        sleep(5)
        # Save button
        self.__click_button(
            "mat-focus-indicator mat-stroked-button mat-button-base btn btn-block btn-brand-orange mat-btn-lg"
        )
        sleep(10)
        self.__select_appointment_book()
        sleep(5)
    
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
            '//a[text()={}]'.format(self.person["FREE_WINDOW"])
            ).click()
        sleep(3)
        #Trying to click on load more button if it works
        try:
            self.__click_button(
                "mat-focus-indicator btn mat-btn-lg btn-block load-more mat-stroked-button mat-button-base mat-button-disabled ng-star-inserted"
            )
        except ElementNotInteractableException:
            pass
        sleep(3)

        #Random choicer of hours
        appointment_hours = self.driver.find_elements(
            By.XPATH,
            "//div[@class='ba-slot-box ng-star-inserted']"
            )
        sleep(3)
        random.choice(appointment_hours).click()

        #Submitt btn
        sleep(4)
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base"
        )
        sleep(5)
        #Next step
        self.__book_review()

    def __book_review(self):
        #Book Review section
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(2)
        self.driver.find_element(By.ID, 'mat-checkbox-1').click()
        sleep(3)
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base mat-button-disabled ng-star-inserted"
        )
        sleep(10)
        self.__fill_bank_data_out()
    
    def __fill_bank_data_out(self):
        # Cart Num
        self.driver.find_element(By.NAME, 'pan').send_keys(self.person["cart_num"])
        sleep(2)
        # Cart expyrity date
        Select(self.find_element(By.NAME, 'Ecom_Payment_Card_ExpDate_Month')).select_by_value(self.person["expiry_month"])
        sleep(2)
        Select(self.find_element(By.NAME, 'Ecom_Payment_Card_ExpDate_Year')).select_by_value(self.person["expiry_year"])
        sleep(2)
        # Person data
        self.driver.find_element(By.NAME, 'Fismi').send_keys(self.person["name_and_surname"])
        sleep(2)
        self.driver.find_element(By.NAME, 'Fadres').send_keys(self.person["address"])
        sleep(2)
        self.driver.find_element(By.NAME, 'Fadres2').send_keys(self.person["city_district_postcode"])
        sleep(1)
        #Check box
        self.driver.find_element(By.NAME, 'sameshipping').click()
        sleep(2)
        # Submitt btn
        self.driver.find_element(By.IDm, 'btnSbmt').click()
        sleep(1000)

    def work(self) -> Any:
        self.__choose_visa_centre()

        self.__choose_visa_category()
        
        self.__choose_visa_subcategory()
        sleep(3)
        
        # Submitt btn for categories
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(4)
        self.driver.find_element(
                            By.XPATH, 
                            "//section/form/mat-card/button/span"
                            ).click()
        sleep(5)
        # Next step of new booking
        self.__fill_person_data_out()

    def generate_report(self) -> Any:
        return super().generate_report()