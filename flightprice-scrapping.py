from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
from email.message import EmailMessage
import ssl
import smtplib
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv() # to load environment variables

# To load website
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# URL 
from_loc = 'JFK'
to_loc = 'BOM'

#Fetch the dates
current_date = datetime.now().date()
next_day = current_date + timedelta(days=1)

#sort  by cheapest price & no layover with 2 stops -> sort=price_a&fs=stops=-2

url=f'https://www.kayak.com/flights/{from_loc}-{to_loc}/{next_day}?sort=price_a&fs=stops=-2'
driver.get(url)

#update time as per the pop-up box
sleep(100)

# To close ad pop-up box
popup_window = '//div[@class = "dDYU-close dDYU-mod-variant-right-corner-inside dDYU-mod-size-default"]'
# popup_window_elements = driver.find_elements(By.XPATH, popup_window)
# # Check if there is any element in the list
# if popup_window_elements:
#     # Click on the first element in the list
#     popup_window_elements[0].click()
# else:
#     print("No pop-up found")

# Explicitly wait for the pop-up element to be clickable
try:
    popup_window_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, popup_window))
    )
    popup_window_element.click()
    print("Pop-up closed successfully.")
except TimeoutException:
    print("Timed out waiting for the pop-up to be clickable.")
except Exception as e:
    print(f"Error closing pop-up: {e}")


# Fetch Flight details
flight_rows = driver.find_elements(By.XPATH, '//div[@class="nrc6-inner"]')

lst_prices = []
company_nm = []
flight_time = []
flight_duration = []
flight_layover = []

for WebElement in flight_rows:
    elementHTML = WebElement.get_attribute('outerHTML')
    elementSoup = BeautifulSoup(elementHTML,'html.parser')

    #price
    temp_price = elementSoup.find("div",{"class": "nrc6-price-section"})
    price = temp_price.find("div",{"class":"f8F1-price-text"})
    lst_prices.append(price.text)

    #flight name
    temp_flight = elementSoup.find("div",{"class":"c_cgF c_cgF-mod-variant-default"})
    company_nm.append(temp_flight.text)

    #flight time
    temp_flight_time = elementSoup.find("div",{"class":"vmXl vmXl-mod-variant-large"})
    time_text = temp_flight_time.get_text()
    flight_time.append(time_text [:-2])

    #layover details
    temp_layover = elementSoup.find("div",{"class":"JWEO"})
    layover_text = temp_layover.get_text()
    if layover_text == 'nonstop':
        flight_layover.append('Nonstop')
    else:
        flight_layover.append(layover_text[-3:])

    #fligh duration
    temp_flight_duration = elementSoup.find("div",{"class":"xdW8"})
    duration_text = temp_flight_duration.get_text(strip=True)
    flight_duration.append(duration_text[:-7])

combined_list = list(map(list, zip(company_nm, flight_time, flight_duration,flight_layover,lst_prices)))

# Print the combined list
# def flight_dets():
#   for flight in combined_list:
#       print(flight)

def flight_dets():
    flights_info = []
    for flight in combined_list:
        flight_info = f"<tr><td>{flight[0]}</td><td>{flight[1]}</td><td>{flight[2]}</td><td>{flight[3]}</td><td>{flight[4]}</td></tr>"
        flights_info.append(flight_info)

    table_header = "<table border='1'><tr><th>Flight Carrier</th><th>Flight Timing</th><th>Flight Duration</th><th>Flight Layover</th><th>Flight Price</th></tr>"
    table_footer = "</table>"
    flights_info_str = "".join(flights_info)
    body = f"Hi Subscriber,<br><br>{table_header}{flights_info_str}{table_footer}<br><br>Thank You,<br>KoolWave"
    return body

# email details
email_sender = os.getenv("email_sender_env")
email_password = os.getenv("email_password_env")
email_receiver = os.getenv("email_receiver_env")
    
subject = "Flight Prices for JFK-BOM flights"
body = flight_dets()

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body, subtype='html')  # Set subtype to 'html' for HTML content

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())