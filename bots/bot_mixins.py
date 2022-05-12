import random
from time import sleep

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

class FormFillerMixin:
    """Forms filler mixin. There\'s ready methods for filling VFS forms here"""

    VISA_CATEGORY = "National Visa (Type D) / Uzun Donem  / Wiza typu D"
    VISA_SUBCATEGORY = "2- Work permit / Calisma Izni / w celu wykonywania pracy"

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

    def choose_visa_centre(self, visa_centre: str) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//mat-form-field/div/div/div[3]"
        ).click()
        sleep(6)

        self.__mat_select(visa_centre)
        sleep(5)

    def choose_visa_category(self) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//div[@id='mat-select-value-3']"
        ).click()
        sleep(6)
        
        self.__mat_select(self.VISA_CATEGORY)
        sleep(5)

    def choose_visa_subcategory(self) -> None:
        #DropDown click
        self.driver.find_element(By.XPATH,
            "//div[@id='mat-select-value-5']"
        ).click()
        sleep(6)
        self.__mat_select(self.VISA_SUBCATEGORY)
        sleep(5)

    def fill_person_data_out(self, person: dict) -> None:
        #First name
        self.driver.find_element(By.ID, 'mat-input-2').send_keys(person["FIRST_NAME"])
        sleep(2)
        #Last name
        self.driver.find_element(By.ID, 'mat-input-3').send_keys(person["LAST_NAME"])
        sleep(2)
        # Gender select
        self.driver.find_element(
            By.XPATH,
            "//div[@id='mat-select-value-7']"
             ).click()
        sleep(2)
        self.__mat_select(person["GENDER"])
        sleep(2)
        #Date of Birth
        self.driver.find_element(By.ID, 'dateOfBirth').send_keys(person["DATE_OF_BIRTH"])
        sleep(2)
        #Citizienship select
        self.driver.find_element(
            By.XPATH, "//div[@id='mat-select-value-9']"
            ).click()
        sleep(2)
        self.__mat_select(person["CITIZIENSHIP"])
        sleep(2)
        #Passport number
        self.driver.find_element(By.ID, 'mat-input-4').send_keys(person["PASSPORT_NUMBER"])
        sleep(2)
        #Passport Expirty Date
        self.driver.find_element(By.ID, 'passportExpirtyDate').send_keys(person["Passport_Expirty_Date"])
        sleep(2)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(2)
        # Phonenumber code without '+'
        self.driver.find_element(By.ID, 'mat-input-5').send_keys(person["PHONE_CODE"])
        sleep(2)
        # Phone number
        self.driver.find_element(By.ID, 'mat-input-6').send_keys(person["PHONE_NUMBER"])
        sleep(2)
        # Email
        self.driver.find_element(By.ID, 'mat-input-7').send_keys(person["EMAIL"])
        sleep(5)
        # Save button
        self.__click_button(
            "mat-focus-indicator mat-stroked-button mat-button-base btn btn-block btn-brand-orange mat-btn-lg"
        )
    
    def select_appointment_book(self, person: dict):
        #Continue button
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base"
        )
        sleep(3)
        #Book Appointment section filling out
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(5)
        self.driver.find_element(
            By.XPATH,
            '//a[text()={}]'.format(person["FREE_WINDOW"])
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

    def book_review(self):
        #Book Review section
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(2)
        self.driver.find_element(By.ID, 'mat-checkbox-1').click()
        sleep(3)
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base mat-button-disabled ng-star-inserted"
        )
    
    def fill_bank_data_out(self, person: dict):
        # Card Num
        self.driver.find_element(By.NAME, 'pan').send_keys(person["cart_num"])
        sleep(2)
        # Card expyrity date
        Select(self.find_element(By.NAME, 'Ecom_Payment_Card_ExpDate_Month')).select_by_value(person["expiry_month"])
        sleep(2)
        Select(self.find_element(By.NAME, 'Ecom_Payment_Card_ExpDate_Year')).select_by_value(person["expiry_year"])
        sleep(2)
        # Person data
        self.driver.find_element(By.NAME, 'Fismi').send_keys(person["name_and_surname"])
        sleep(2)
        self.driver.find_element(By.NAME, 'Fadres').send_keys(person["address"])
        sleep(2)
        self.driver.find_element(By.NAME, 'Fadres2').send_keys(person["city_district_postcode"])
        sleep(1)
        #Check box
        self.driver.find_element(By.NAME, 'sameshipping').click()
        sleep(2)
        # Submitt btn
        self.driver.find_element(By.IDm, 'btnSbmt').click()
        sleep(1000)
    
class LoginMixin:
    """Login Form Filler"""
    
    URL = "https://visa.vfsglobal.com/tur/en/pol/login"

    def login(self, email: str, password: str) -> None:
        self.driver.get(self.URL)
        sleep(15)
        try:
            self.driver.find_element(By.ID, 'mat-input-0').send_keys(email)
            sleep(2)
            self.driver.find_element(By.ID, 'mat-input-1').send_keys(password)
            sleep(2)
            self.driver.find_element(By.CLASS_NAME, 'mat-btn-lg').click()
            sleep(15)
            self.driver.find_element(By.ID, 'onetrust-close-btn-container').click()
        except:
            print("Email or password was given incorrect!")