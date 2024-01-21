from time import sleep
import pandas as pd 
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from selenium.webdriver import chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta

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

# sleep(180)

# To close ad pop-up box
popup_window = '//div[@class = "dDYU-close dDYU-mod-variant-right-corner-inside dDYU-mod-size-default"]'
popup_window_elements = driver.find_elements(By.XPATH, popup_window)
# Check if there is any element in the list
if popup_window_elements:
    # Click on the first element in the list
    popup_window_elements[0].click()
else:
    print("No pop-up found")


# Fetch Flight details
flight_rows = driver.find_elements(By.XPATH, '//div[@class="nrc6-inner"]')

lst_prices = []
company_nm = []
flight_time = []
flight_duration = []

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

    #fligh duration
    temp_flight_duration = elementSoup.find("div",{"class":"xdW8"})
    duration_text = temp_flight_duration.get_text(strip=True)
    flight_duration.append(duration_text[:-7])

combined_list = list(zip(company_nm, flight_time, flight_duration,lst_prices))

# Print the combined list
for flight in combined_list:
    print(flight)

   