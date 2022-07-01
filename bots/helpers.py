from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def find_element_with_retry_base(driver, element_locator, by):
    wait_time = 10
    retries = 1
    while retries <= 3:
        try:
            return WebDriverWait(
                driver, wait_time).until(
                    ec.presence_of_element_located((by, element_locator)))
        except TimeoutException:
            wait_time += 5
            retries += 1
            driver.refresh()


def find_element_with_retry_by_id(driver, element_id):
    return find_element_with_retry_base(driver, element_id, By.ID)


def find_element_with_retry_by_class(driver, element_class):
    return find_element_with_retry_base(driver, element_class, By.CLASS_NAME)
