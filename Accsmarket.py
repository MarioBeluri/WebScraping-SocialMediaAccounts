from hashlib import new
from telnetlib import EC

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from time import sleep
from pymongo import MongoClient
from utils.logging import logger as LOGGER


social_media_urls = {
    "Twitter": "https://accsmarket.com/en/catalog/twitter",
    "Instagram": "https://accsmarket.com/en/catalog/instagram",
    "Facebook": "https://accsmarket.com/en/catalog/facebook"
}

def scrape_data(driver, url, social_media):
    driver.get(url)
    sleep(10)
    listings = driver.find_elements(By.XPATH, "//div[@class = 'soc-text']/p/a")

    quantity = [quantity.text.split()[0] for quantity in driver.find_elements(By.XPATH, "//div[@class = 'soc-qty']")]
    URls = [url.get_attribute("href") for url in driver.find_elements(By.XPATH, "//div[@class = 'soc-text']/p/a")]
    prices = [price.get_attribute("textContent") for price in
              driver.find_elements(By.XPATH, "//div[@class = 'soc-price']/div")]
    descriptions = [listing.get_attribute("text") for listing in listings]
    social_medias = [social_media for _ in range(len(listings))]

    for i in range(len(prices)):
        index_of_dollar = prices[i].find('$')
        if index_of_dollar != -1:
            prices[i] = prices[i][index_of_dollar:].strip().replace("$", "")

    try:
        client = MongoClient()
        db = client.WebScraping
        collection = db.WebScraping
        for j in range(len(listings)):
            entry_data = {
                "url": URls[j],
                "title": descriptions[j],
                "quantity": int(quantity[j]),
                "price": float(prices[j]),
                "social_media": social_medias[j]
            }
            collection.insert_one(entry_data)
    except:
        LOGGER.info("Error Occured")
    finally:
        client.close()
        LOGGER.info("Conenction Closed")

# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, Facebook): ")

# Validate user input and scrape data accordingly
if social_media_input in social_media_urls:
    driver = Driver(uc=True)
    scrape_data(driver, social_media_urls[social_media_input], social_media_input)
    driver.quit()
    LOGGER.info("Scraping finished")
else:
    LOGGER.info("Invalid social media platform. Please enter a valid Social Media platform.")
