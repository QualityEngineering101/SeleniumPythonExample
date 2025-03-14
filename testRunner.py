from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from OpenAIAPI import OpenAIAPI
from WebUI import WebUI
# Declare global variable
driver = None

URL = "https://katalon-demo-cura.herokuapp.com/profile.php#login"

def initialize_driver():
    global driver
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()

    # Initialize the driver (e.g., ChromeDriver in this case)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def main():
    global driver
    global openAI
    global webUI

    # Initialize the driver
    initialize_driver()

    # Initialize the WebUI
    webUI = WebUI(driver)

    # Open a webpage
    webUI.navigateToURL(URL)

    # Initialize the OpenAI API
    openAI = OpenAIAPI(driver)

    # Initialize the WebUI
    webUI = WebUI(driver)
    
    print ("Webpage opened")

    ############# LOGIN #############

    # Create object repository
    openAI.create_object_repository()

    # log in
    webUI.set_text(openAI.find_element("username"), "John Doe")
    webUI.set_text(openAI.find_element("password"), "ThisIsNotAPassword")
    webUI.click(openAI.find_element("login"))
    driver.implicitly_wait(1000)

    ############# APPOINTMENT #############

    # Create object repository
    openAI.create_object_repository()

    # Find an element by its ID and interact with it (example: search box)
    buttonAppointment =  findElementByID("btn-make-appointment")

    # click on button
    buttonAppointment.click()

    #search_box.send_keys("Selenium WebDriver" + Keys.RETURN)

    # Wait for the results to load (you can also use WebDriverWait for more advanced waiting)
    driver.implicitly_wait(100)

    # Close the browser
    driver.quit()

def findElementByID(identifier):
    try:
        WebElement = driver.find_element(By.ID, identifier)
        print ("Element found: " + identifier)
        return WebElement

    except NoSuchElementException:
        print ("Element not found:" + identifier)


#def findXPathUsingAI(String fieldName):

# Call the main function to run the program
if __name__ == "__main__":
    main()