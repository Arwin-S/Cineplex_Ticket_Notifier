import requests
from bs4 import BeautifulSoup
from time import time

# URL of the website page you want to scrape
url = "https://www.cineplex.com/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the element you want to monitor for changes
element = soup.find("h1", class_="header")


# print(element)
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
