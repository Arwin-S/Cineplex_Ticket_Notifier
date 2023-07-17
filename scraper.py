from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

from bs4 import BeautifulSoup
import time
from twilio.rest import Client

from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

import gmailer as gmailer


def web_scraper(day) -> int:
    # Set up Selenium WebDriver (you may need to specify the path to your WebDriver executable)
    driver = webdriver.Chrome()

    # Load the initial page
    driver.get("https://www.cineplex.com/theatre/scotiabank-theatre-toronto")
    time.sleep(5)

    # Find the button using text
    driver.find_element(By.XPATH, '//button[normalize-space()="Get Tickets"]').click()
    time.sleep(10)

    # Find the button using text
    driver.find_element(
        By.XPATH, '//button[@type="button" and @data-name="select-Date"]'
    ).click()
    time.sleep(5)

    # Get the updated page source after the button click
    updated_page_source = driver.page_source

    # Close the Selenium WebDriver
    driver.quit()

    # Parse the updated page source using BeautifulSoup
    soup = BeautifulSoup(updated_page_source, "html.parser")

    # Find the element you want to monitor for changes
    elements = soup.find_all("h4")

    if elements:
        return len(list(filter(lambda d: d.text.strip() == day, elements)))
    else:
        return 0  # No days found (scraper broken)


def notify(status, client):
    if status == True:
        print("Tickets are available")
        message = client.messages.create(
            body="TICKETS AVAILABLE https://www.cineplex.com/theatre/scotiabank-theatre-toronto",
            from_=from_phone_num,
            to=to_phone_num,
        )
    else:
        print("Web Scraper Broken")
        message = client.messages.create(
            body="SCRAPER BROKEN", from_=from_phone_num, to=to_phone_num
        )
    print(message.sid)


if __name__ == "__main__":
    with open("credentials.yaml", "r") as file:
        creds = yaml.safe_load(file)

    account_sid = creds["account_sid"]
    auth_token = creds["auth_token"]
    to_phone_num = creds["to_phone_num"]
    from_phone_num = creds["from_phone_num"]
    email = creds["email"]

    # Scopes for Gmail API access
    scopes = ["https://www.googleapis.com/auth/gmail.send"]

    # Path to the JSON file for storing credentials
    credentials_json = "credentials.json"

    # Perform OAuth flow to obtain credentials
    flow = InstalledAppFlow.from_client_secrets_file(credentials_json, scopes)
    credentials = flow.run_local_server()

    # Create a Gmail API client using the credentials
    service = build("gmail", "v1", credentials=credentials)

    # print(account_sid, auth_token, to_phone_num, from_phone_num, email)

    client = Client(account_sid, auth_token)

    # Send start text to test API and creds working
    message = client.messages.create(
        body="Starting Scraper.  https://www.cineplex.com/theatre/scotiabank-theatre-toronto",
        from_=from_phone_num,
        to=to_phone_num,
    )

    # Send starting email

    subject = "[CinNotif] STARTING " + datetime.now().strftime("%H:%M %D")
    body = "https://www.cineplex.com/theatre/scotiabank-theatre-toronto"
    sender = email
    recipients = [email]

    email_message = gmailer.create_message(sender, sender, subject, body)
    gmailer.send_message(service, "me", email_message)

    day = "Saturday"
    # day = 'Wednesday'

    email_q = 0
    email_q_thresh = 10

    while True:
        try:
            numDays = web_scraper(day)

            # Notify text
            if numDays > 1:
                notify(True, client)

            # Don't notify text: Dates not available
            else:
                if numDays != 1:
                    # Update Email Status: error with scraper
                    subject = "[CinNotif] SCRAPER ERROR " + datetime.now().strftime(
                        "%H:%M %D"
                    )
                else:
                    # Update Email Status: Dates not available yet
                    subject = "[CinNotif] STILL WAITING " + datetime.now().strftime(
                        "%H:%M %D"
                    )

                email_message = gmailer.create_message(
                    sender, sender, subject, str(numDays) + "\n" + body
                )

                # Only send email every x amount of loops
                if email_q >= email_q_thresh:
                    gmailer.send_message(service, "me", email_message)
                    email_q = 0
                else:
                    email_q += 1

        # Selenium scraper didn't work
        except Exception as e:
            # notify(False, client)

            # Update Email Status: error with scraper
            subject = "[CinNotif] SCRAPER ERROR " + datetime.now().strftime("%H:%M %D")

            email_message = gmailer.create_message(sender, sender, subject, body)
            gmailer.send_message(service, "me", email_message)

        time.sleep(30)
