from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class WebUI:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, name):
        return self.driver.find_element(By.XPATH, name)

    def set_text(self, element: WebElement, text: str):
        element.send_keys(text)

    def click(self, element: WebElement):
        element.click()

#WebUI.setText(findTestObject('Object Repository/Page_CURA Healthcare Service/input_Username_username'), 'John Doe')
