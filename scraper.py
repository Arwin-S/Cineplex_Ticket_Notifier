from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
# Set up Selenium WebDriver (you may need to specify the path to your WebDriver executable)
driver = webdriver.Chrome()

# Load the initial page
driver.get("https://www.cineplex.com/theatre/scotiabank-theatre-toronto")
time.sleep(2)

# Find the button using text
driver.find_element(By.XPATH, '//button[normalize-space()="Get Tickets"]').click()

# Wait for the side pane to load (adjust the wait time as needed)
time.sleep(2)

# Find the button using text
driver.find_element(By.XPATH, '//button[@type="button" and @data-name="select-Movie"]').click()
time.sleep(5)

# Get the updated page source after the button click
updated_page_source = driver.page_source

# Close the Selenium WebDriver
driver.quit()

# Parse the updated page source using BeautifulSoup
soup = BeautifulSoup(updated_page_source, "html.parser")


# Find the element you want to monitor for changes
elements = soup.find_all(attrs={"data-name": True})
if elements:
    for element in elements:
        print(element.text.strip())
else:
    print("Element not found.")
    
    
# # Save the initial content of the element
# initial_content = element.text.strip()

# # Function to check for changes in the element
# def check_for_changes():
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     updated_element = soup.find("h1", class_="header")
#     updated_content = updated_element.text.strip()
    
#     if updated_content != initial_content:
#         print("The element has changed!")
#         print("Old content:", initial_content)
#         print("New content:", updated_content)
#         # Add your notification mechanism here
#     else:
#         print("No changes detected.")

# # Run the change detection function periodically
# # You can customize the frequency and duration as per your needs
# while True:
#     check_for_changes()
#     time.sleep(60)  # Wait for 60 seconds before checking again
