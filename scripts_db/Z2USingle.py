import time
from hashlib import new
from telnetlib import EC

from pymongo import MongoClient
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from utils.logging import logger as LOGGER


def scrape_data(driver, url, social_media, collection):
    driver.get(url)
    time.sleep(15)

    URL = url

    try:
        title = driver.find_element(By.XPATH, "//div[@class = 'combin-light-bg-wrap']/h2").text
    except Exception as e:
        LOGGER.info("Error finding title:", e)
        title = None

    try:
        seller = driver.find_element(By.CLASS_NAME, 'seller__name').text
    except Exception as e:
        LOGGER.info("Error finding seller:", e)
        seller = None

    try:
        info_element = driver.find_element(By.CSS_SELECTOR, ".boxbottom.dengji.flex_between .u-info li")
        text = info_element.text
        parts = text.split("\n")
        total_order = int(parts[0].split(": ")[1])
        positive_rating = parts[1].split(': ')[1].split(' ')[0]
        positive_review = int(parts[1].split('(')[1].split(')')[0])
    except Exception as e:
        LOGGER.info("Error finding seller info:", e)
        total_order = None
        positive_rating = None
        positive_review = None

    try:
        offer_id = int(driver.find_element(By.CLASS_NAME, "wenbenright").text.split('#')[1])
    except Exception as e:
        LOGGER.info("Error finding offer id:", e)
        offer_id = None

    try:
        offer = int(driver.find_element(By.CSS_SELECTOR, ".more-offers strong").text)
    except Exception as e:
        LOGGER.info("Error finding offers:", e)
        offer = None

    try:
        price = float(driver.find_element(By.CLASS_NAME, "price").text.replace(',', ''))
    except Exception as e:
        LOGGER.info("Error finding price:", e)
        price = None

    try:
        description = driver.find_element(By.CLASS_NAME, "wb_text_in").text
    except Exception as e:
        LOGGER.info("Error finding description:", e)
        description = None

    social_medias = social_media

    try:
        entry_data = {
            "url": URL,
            "title": title,
            "seller": seller,
            "total_order": total_order,
            "rating_pct": positive_rating,
            "rating_count": positive_review,
            "offer_id": offer_id,
            "pending_offers": offer,
            "description": description,
            "price": price,
            "social_media": social_medias
        }
        collection.insert_one(entry_data)
    except Exception as e:
        LOGGER.info("Error Occurred:", e)
        client.close()
        LOGGER.info("Connection Closed")
    time.sleep(15)


# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, Facebook): ")

# Validate user input and scrape data accordingly
driver = Driver(uc=True, headed=True)
client = MongoClient()
db = client.WebScraping
collection = db.Z2UFillerFacebook

login = "https://www.z2u.com/"

driver.get(login)
time.sleep(100)

try:
    # Open the file in read mode
    with open(r'/home/c01mabe/Downloads/Z2UFacebookMissing.txt', 'r') as file:
        # Read each line (URL) from the file
        for line in file:
            # Process each URL
            url = line.strip()  # Remove leading/trailing whitespaces
            scrape_data(driver, url, social_media_input, collection)
except FileNotFoundError:
    print("File not found at the given path.")
except Exception as e:
    print("An error occurred:", str(e))

client.close()
LOGGER.info("Connection Closed")
driver.quit()
LOGGER.info("Web Scraping finished")