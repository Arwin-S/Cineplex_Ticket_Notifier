from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
from twilio.rest import Client
import getpass


def web_scraper(day) -> int:
    # Set up Selenium WebDriver (you may need to specify the path to your WebDriver executable)
    driver = webdriver.Chrome()

    # Load the initial page
    driver.get("https://www.cineplex.com/theatre/scotiabank-theatre-toronto")
    time.sleep(5)

    # Find the button using text
    driver.find_element(By.XPATH, '//button[normalize-space()="Get Tickets"]').click()
    time.sleep(8)

    # Find the button using text
    driver.find_element(By.XPATH, '//button[@type="button" and @data-name="select-Date"]').click()
    time.sleep(5)

    # driver.find_element(By.TAG_NAME, 'h4')
    # time.sleep(5)

    # Get the updated page source after the button click
    updated_page_source = driver.page_source

    # Close the Selenium WebDriver
    driver.quit()

    # Parse the updated page source using BeautifulSoup
    soup = BeautifulSoup(updated_page_source, "html.parser")


    # Find the element you want to monitor for changes
    elements = soup.find_all('h4')

    if elements:
        return len(list(filter(lambda d: d.text.strip() == day, elements)))
    else:
        return 0 # No days found (scraper broken)
    
def notify(status, client):
    if status == True:
        print('Tickets are available')
        message = client.messages.create(
            body='TICKETS AVAILABLE',
            from_=from_phone_num,
            to=to_phone_num
        )
    else:
        print('Web Scraper Broken')
        message = client.messages.create(
            body='SCRAPER BROKEN',
            from_=from_phone_num,
            to=to_phone_num
        )
    print(message.sid)
    
    
if __name__ == '__main__':
    
    account_sid = getpass.getpass("Account SID:")
    auth_token = getpass.getpass("Auth Token:")
    to_phone_num = getpass.getpass("Phone Number to Notify:")
    from_phone_num = getpass.getpass("Phone Number to Send From:")
    

    
    client = Client(account_sid, auth_token)
    
    day = 'Saturday'
    # day = 'Wednesday'
    while(True):
        numDays = web_scraper(day)
        if numDays == 0:
            notify(False, client)
        elif numDays > 1:
            notify(True, client)
        else:
        
        time.sleep(10)
