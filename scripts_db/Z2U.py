import time
from hashlib import new
from telnetlib import EC

from pymongo import MongoClient
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from utils.logging import logger as LOGGER

social_media_urls = {
    "Twitter": "https://www.z2u.com/twitter/accounts-5-15142",
    "Instagram": "https://www.z2u.com/instagram/accounts-5-15129",
    "Facebook": "https://www.z2u.com/facebook/accounts-5-15128"
}


def get_next_page():
    """
    script to navigate to next page
    """
    script = """
    var nextLink = document.querySelector('a.next');    
    nextLink.click();
    """
    return script


def scrape_data(driver, url, social_media, collection):
    login = "https://www.z2u.com/"

    driver.get(login)
    time.sleep(40)
    driver.get(url)
    time.sleep(5)

    for _ in range(15):
        script = get_next_page()
        driver.execute_script(script)
        time.sleep(10)

    while True:

        elements = driver.find_elements("xpath", "//div[@class = 'row wrapper shop_list']/div//a")

        for element in elements:
            link = element.get_attribute("href")
            original_window = driver.current_window_handle
            URL = link

            driver.switch_to.new_window('tab')
            driver.get(link)
            time.sleep(20)

            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    break

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

            driver.close()
            driver.switch_to.window(original_window)
            time.sleep(20)

        try:
            script = get_next_page()
            driver.execute_script(script)
            time.sleep(7)
        except Exception as e:
            print("Next Page error")
            break


# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, Facebook): ")

# Validate user input and scrape data accordingly
if social_media_input in social_media_urls:
    driver = Driver(uc=True, headed=True)
    client = MongoClient()
    db = client.WebScraping
    collection = db.Z2U
    scrape_data(driver, social_media_urls[social_media_input], social_media_input, collection)
    client.close()
    LOGGER.info("Connection Closed")
    driver.quit()
    LOGGER.info("Web Scraping finished")
else:
    LOGGER.info("Invalid social media platform. Please enter a valid Social Media platform.")