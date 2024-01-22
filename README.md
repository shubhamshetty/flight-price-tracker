# Flight Price Tracking Scraper

This Python script is designed to scrape flight prices from Kayak for a specific route and date, and send the information via email. The script utilizes Selenium for web scraping, BeautifulSoup for parsing HTML, and smtplib for sending emails.

## Prerequisites

Before running the script, ensure you have the necessary dependencies installed. You can install them using the following command:

```bash
pip install -r requirements.txt
```

Make sure to have the latest version of ChromeDriver installed by running:

```bash
webdriver-manager update --chrome
```

Create a `.env` file in the project directory with the following variables:

```dotenv
email_sender_env=your_email@gmail.com
email_password_env=your_email_password
email_receiver_env=recipient_email@gmail.com
```

## Usage

1. Set the departure and destination locations:

```python
from_loc = 'JFK'
to_loc = 'BOM'
```

2. Adjust the URL based on your requirements:

```python
url = f'https://www.kayak.com/flights/{from_loc}-{to_loc}/{next_day}?sort=price_a&fs=stops=-2'
```

3. Run the script:

```bash
python flight_scraper.py
```

## Script Overview

- The script launches a Chrome browser using Selenium and navigates to the specified Kayak URL.
- It closes any pop-up windows that may appear.
- It extracts flight details such as carrier, timing, duration, and price using BeautifulSoup.
- The information is formatted into an HTML table.
- The script sends an email with the flight details using the provided Gmail credentials.

## Note

- Make sure to use this script responsibly.
- Update the email credentials in the `.env` file.
- For security reasons, consider using an 'App Password' for Gmail instead of your account password.
- Customize the email subject and body according to your preferences.
