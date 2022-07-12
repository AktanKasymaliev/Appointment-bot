import random
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from bots.constants import HEAVY_TIMEOUT
from bots.constants import LIGHT_TIMEOUT
from bots.constants import MEDIUM_TIMEOUT
from bots.support_funcs import find_element_with_retry_by_id
from bots.support_funcs import find_element_with_retry_by_class
from bots.support_funcs import find_element_with_retry_by_xpath
from bots.support_funcs import is_firewall_blocked_at_the_end
from bots.support_funcs import is_firewall_blocked_at_the_start
from bots.support_funcs import random_sleep


class FormFillerMixin:
    """Forms filler mixin. There\'s ready methods for filling VFS forms here"""

    VISA_CATEGORY = "National Visa (Type D) / Uzun Donem  / Wiza typu D"

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def __click_button(self, class_name: str) -> None:
        self.driver.find_element(
            By.XPATH, "//button[@class='{}']/span".format(class_name)
            ).click()
    
    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def click_submit_on_categories(self):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//section/form/mat-card/button/span"))
        ).click() 
        sleep(MEDIUM_TIMEOUT)
    
    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def __mat_select(self, arg: str) -> None:
        """
        It clicks on the dropdown menu, then clicks on the option that matches the argument
        
        :param arg: The name of the visa centre you want to select
        :type arg: str
        """
        try:
            xpath = "//mat-option/span[contains(text(), '{}')]".format(arg)
            opt = find_element_with_retry_by_xpath(self.driver, xpath)
            if not opt:
                raise NoSuchElementException(f"Coundn't select {arg}")
            opt.click()
            random_sleep()
        except NoSuchElementException:
            raise NoSuchElementException("Value not found: {}".format(arg))


    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def choose_visa_centre(self, visa_centre: str) -> None:
        sleep(LIGHT_TIMEOUT)
        #DropDown click
        visa_center_dropdown = find_element_with_retry_by_xpath(self.driver, "//mat-form-field/div/div/div[3]")
        if not visa_center_dropdown:
            raise NoSuchElementException("Visa center dropdown couldn't be found")
        visa_center_dropdown.click()
        random_sleep()
        self.__mat_select(visa_centre)

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def choose_visa_category(self) -> None:
        #DropDown click
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//div[@id='mat-select-value-3']"))
        ).click()
        random_sleep()
        self.__mat_select(self.VISA_CATEGORY)

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def choose_visa_subcategory(self, subcategory: str) -> None:
        #DropDown click
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//div[@id='mat-select-value-5']"))
        ).click()
        random_sleep()
        self.__mat_select(subcategory)

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def fill_person_data_out(self, person: dict) -> None:
        #First name
        self.driver.find_element(By.ID, 'mat-input-2').send_keys(person["FIRST_NAME"])
        sleep(LIGHT_TIMEOUT)
        #Last name
        self.driver.find_element(By.ID, 'mat-input-3').send_keys(person["LAST_NAME"])
        sleep(LIGHT_TIMEOUT)
        # Gender select
        self.driver.find_element(
            By.XPATH,
            "//div[@id='mat-select-value-7']"
            ).click()
        sleep(LIGHT_TIMEOUT)
        self.__mat_select(person["GENDER"])
        sleep(LIGHT_TIMEOUT)
        #Date of Birth
        self.driver.find_element(By.ID, 'dateOfBirth').send_keys(person["DATE_OF_BIRTH"])
        sleep(LIGHT_TIMEOUT)
        #Citizienship select
        self.driver.find_element(
            By.XPATH, "//div[@id='mat-select-value-9']"
            ).click()
        sleep(LIGHT_TIMEOUT)
        self.__mat_select(person["CITIZIENSHIP"].upper())
        sleep(LIGHT_TIMEOUT)
        #Passport number
        self.driver.find_element(By.ID, 'mat-input-4').send_keys(person["PASSPORT_NUMBER"])
        sleep(LIGHT_TIMEOUT)
        #Passport Expirty Date
        self.driver.find_element(By.ID, 'passportExpirtyDate').send_keys(person["Passport_Expirty_Date"])
        sleep(LIGHT_TIMEOUT)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(LIGHT_TIMEOUT)
        # Phonenumber code without '+'
        self.driver.find_element(By.ID, 'mat-input-5').send_keys(person["PHONE_CODE"])
        sleep(LIGHT_TIMEOUT)
        # Phone number
        self.driver.find_element(By.ID, 'mat-input-6').send_keys(person["PHONE_NUMBER"])
        sleep(LIGHT_TIMEOUT)
        # Email
        self.driver.find_element(By.ID, 'mat-input-7').send_keys(person["EMAIL"])
        sleep(MEDIUM_TIMEOUT)
        # Save button
        self.__click_button(
            "mat-focus-indicator mat-stroked-button mat-button-base btn btn-block btn-brand-orange mat-btn-lg"
        )

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def select_appointment_book(self, person: dict):
        #Continue button
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base"
        )
        sleep(MEDIUM_TIMEOUT)
        #Book Appointment section filling out
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(MEDIUM_TIMEOUT)
        self.driver.find_element(
            By.XPATH,
            '//a[text()={}]'.format(person["FREE_WINDOW"])
            ).click()
        sleep(MEDIUM_TIMEOUT)
        #Trying to click on load more button if it works
        try:
            self.__click_button(
                "mat-focus-indicator btn mat-btn-lg btn-block load-more mat-stroked-button mat-button-base mat-button-disabled ng-star-inserted"
            )
        except ElementNotInteractableException:
            pass
        sleep(LIGHT_TIMEOUT)

        #Random choicer of hours
        appointment_hours = self.driver.find_elements(
            By.XPATH,
            "//div[@class='ba-slot-box ng-star-inserted']"
            )
        sleep(MEDIUM_TIMEOUT)
        random.choice(appointment_hours).click()

        #Submitt btn
        sleep(MEDIUM_TIMEOUT)
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base"
        )

    @is_firewall_blocked_at_the_start
    @is_firewall_blocked_at_the_end
    def book_review(self):
        #Book Review section
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(MEDIUM_TIMEOUT)
        self.driver.find_element(By.ID, 'mat-checkbox-1').click()
        sleep(MEDIUM_TIMEOUT)
        self.__click_button(
            "mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base ng-star-inserted"
        )
    
    def fill_bank_data_out(self, person: dict):
        # Card Num
        self.driver.find_element(By.NAME, 'pan').send_keys(person["cart_num"])
        sleep(LIGHT_TIMEOUT)
        # Card expyrity date
        Select(self.driver.find_element(By.NAME, 'Ecom_Payment_Card_ExpDate_Month')).select_by_value(person["expiry_month"])
        sleep(LIGHT_TIMEOUT)
        Select(self.driver.find_element(By.NAME, 'Ecom_Payment_Card_ExpDate_Year')).select_by_value(person["expiry_year"])
        sleep(LIGHT_TIMEOUT)
        # Person data
        self.driver.find_element(By.NAME, 'Fismi').send_keys(person["name_and_surname"])
        sleep(LIGHT_TIMEOUT)
        self.driver.find_element(By.NAME, 'Fadres').send_keys(person["address"])
        sleep(LIGHT_TIMEOUT)
        self.driver.find_element(By.NAME, 'Fadres2').send_keys(person["city_district_postcode"])
        sleep(LIGHT_TIMEOUT)
        #Check box
        self.driver.find_element(By.NAME, 'sameshipping').click()
        sleep(LIGHT_TIMEOUT)
        # Submitt btn
        self.driver.find_element(By.IDm, 'btnSbmt').click()
        sleep(1000)


class LoginMixin:
    """Login Form Filler"""
    
    URL = "https://visa.vfsglobal.com/tur/en/pol/login"

    @is_firewall_blocked_at_the_start
    def __click_new_booking(self):
        # Wait until loading spinner is gone
        print('Checking if the spinner is gone')
        WebDriverWait(
            self.driver, MEDIUM_TIMEOUT
        ).until(
            ec.invisibility_of_element_located(
                (By.XPATH, "//div[@class='ngx-overlay loading-foreground']")
            )
        )
        print('The spinner is gone. Now trying to click on the "Start New Booking" button.')
        # and try to find the button
        booking_btn = find_element_with_retry_by_xpath(
            self.driver,
            '//section/div/div[2]/button/span',
            refresh=True)
        if not booking_btn:
            raise NoSuchElementException("Couldn't find the booking button")
        booking_btn.click()
        sleep(MEDIUM_TIMEOUT)

    @is_firewall_blocked_at_the_end
    def login(self, email: str, password: str) -> None:
        self.driver.get(self.URL)
        sleep(HEAVY_TIMEOUT)
        try:
            email_inp = find_element_with_retry_by_id(self.driver, 'mat-input-0', refresh=True)
            if not email_inp:
                raise NoSuchElementException("Email input couldn't be found")
            email_inp.send_keys(email)
            sleep(LIGHT_TIMEOUT)
            pass_inp = find_element_with_retry_by_id(self.driver, 'mat-input-1', refresh=True)
            if not pass_inp:
                raise NoSuchElementException("Password input couldn't be found")
            pass_inp.send_keys(password)
            sleep(LIGHT_TIMEOUT)
            btn = find_element_with_retry_by_class(self.driver, 'mat-btn-lg', refresh=True)
            if not btn:
                raise NoSuchElementException("'Sign In' button couldn't be found")
            btn.click()
            sleep(HEAVY_TIMEOUT)
            one_trust_btn = find_element_with_retry_by_id(self.driver, 'onetrust-close-btn-container', refresh=False)
            if one_trust_btn:
                one_trust_btn.click()
            else:
                print("Onetrust btn container couldn't be found. Continuing.")
            self.__click_new_booking()
        except NoSuchElementException as e:
            print("Login to VFS failed")
            print(e)