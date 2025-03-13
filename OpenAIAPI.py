from openai import OpenAI
from selenium.webdriver.common.by import By
import json
import os
from dotenv import load_dotenv
import re

file_path = "object_repository.json"

class OpenAIAPI:
    def __init__(self, driver):
        self.api_key = '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'
        self.model = "gpt-4o-mini"
        self.driver = driver

    def get_page_objects_html(self: str) -> str:
          # Find all input boxes and buttons
        elements = self.driver.find_elements(By.XPATH, "//input | //button")
        
        html_content = ""
        
        # Get HTML content of all elements
        for element in elements:
            # Get element's placeholder, name, or text for matching
            html_content += element.get_attribute("outerHTML")

        print("Retrieved HTML content")
        
        return html_content

    def create_object_repository(self) -> str:
        # Load environment variables
        #load_dotenv()
        
        # Get HTML content of all elements
        html_content = self.get_page_objects_html()

        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an Automation Tester.
                        You need to find XPath of elements on a webpage.
                        Please do the following:
                        1) Scan the HTML provided by the user
                        2) List all input element, including submit button,names and xpath
                        3) Do not include any element with "readonly" attribute
                        4) If there is a button, make sure to include the text of the button in the name
                        5) Name should be unique and lowercase
                        6) Return output in JSON format.  Here's an example:
                            {
                            "fields": [
                                {
                                "name": "username",
                                "xpath": "//input[@id='txt-username']"
                                },
                                {
                                "name": "password",
                                "xpath": "//input[@id='txt-password']"
                                },
                                {
                                    "name": "login",
                                    "xpath": "//button[@id='btn-login']"
                                }
                            ]
                        }
                        """
                },
                {
                    "role": "user",
                    "content": f"HTML: {html_content}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        # Extract the XPath from the response
        try:
            response_content = response.choices[0].message.content
            
            # Parse the JSON string to ensure it's valid
            json_data = json.loads(response_content)
            
            # Save the response to a file (without double-encoding)
            with open(file_path, 'w') as f:
                json.dump(json_data, f, indent=2)
            
            print("Object repository created")

            return True
            
        except Exception as e:
            raise Exception(f"Failed to get valid XPaths from API response: {str(e)}")

    def get_object_repository(self) -> dict:
        with open(file_path, 'r') as f:
            content = f.read()
            # Parse the string twice since it's double-encoded
            return json.loads(content)

    def find_element(self, name: str) -> str:
        print("Finding element: " + name)
        object_repository = self.get_object_repository()
        
        if "fields" not in object_repository:
            print("No fields found in repository")
            return None

        #print("Object repository:", json.dumps(object_repository, indent=2))

        for element in object_repository["fields"]:
            if element["name"] == name:
                WebElement = self.driver.find_element(By.XPATH, element["xpath"])
                print("Element found: " + element["xpath"])
                return WebElement
            
        print("Element not found: " + name)

        raise Exception("Element not found: " + name)

        return None

# Example usage
#if __name__ == "__main__":
#    try:
#        xpath = get_xpath_OpenAI("https://katalon-demo-cura.herokuapp.com/", "Username")
#        print(f"Found XPath: {xpath}")
#    except Exception as e:
#        print(f"Error: {e}")