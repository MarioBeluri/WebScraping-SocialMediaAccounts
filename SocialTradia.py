from hashlib import new
from telnetlib import EC
import re

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from utils.logging import logger as LOGGER
from pymongo import MongoClient
import humanfriendly
import re
from time import sleep

driver = Driver(uc=True)
client = MongoClient()
db = client.WebScraping
collection = db.SocialTradia

website = "https://socialtradia.com/product-categories/"  # Categories

driver.get(website)

number_of_categories = driver.find_elements(By.XPATH, "//div[1]/div/div[1]/div[3]/div/div[@class='nm_column col-sm-4 mt-4']/a")

for categories in number_of_categories:

    categories_link = categories.get_attribute("href")
    original_window = driver.current_window_handle

    driver.switch_to.new_window('tab')
    driver.get(categories_link)
    sleep(5)
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break
    sleep(5)

    while True:

        try:
            names_elements = driver.find_elements(By.XPATH,
                                                  "//div[@class = 'nm-shop-loop-details']/h3/a")
        except Exception as e:
            LOGGER.info("Error occurred while extracting list information:", e)

        try:
            category_element = driver.find_element(By.XPATH,
                                                   "/html/body/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/h1/span")
            categorie = category_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting category information:", e)

        for element in names_elements:
            element_link = element.get_attribute("href")
            original_window_2 = driver.current_window_handle

            driver.switch_to.new_window('tab')
            driver.get(element_link)
            URL = element_link
            sleep(5)
            for handle in driver.window_handles:
                if handle != original_window_2 and handle != original_window:
                    driver.switch_to.window(handle)
                    break
            sleep(5)

            try:
                name_element = driver.find_element(By.CLASS_NAME, "product_title")
                name_and_followers = name_element.text.split("(")

                name = name_and_followers[0].strip()
                subscribed_number = name_and_followers[1].split(")")[0].strip().lower()
            except Exception as e:
                LOGGER.info("Error occurred while extracting name information:", e)
                name = "NotFound"
                subscribed_number = 0

            try:
                price_element = driver.find_element(By.CLASS_NAME, "woocommerce-Price-amount")
                price = float(price_element.text.replace("$", "").replace(",", ""))
            except Exception as e:
                LOGGER.info("Error occurred while extracting price information:", e)
                price = float("0")

            try:
                offers_pending_element = driver.find_element(By.CLASS_NAME, "ofw-info")
                offers = int(offers_pending_element.text.split()[0])
            except Exception as e:
                LOGGER.info("Error occurred while extracting offer information:", e)
                offers = int("0")

            try:
                stock_element = driver.find_element(By.CLASS_NAME, "stock")
                stock = int(stock_element.text.split()[0])
            except Exception as e:
                LOGGER.info("Error occurred while extracting stock information:", e)
                stock = int("0")

            try:
                description_element = driver.find_element(By.CLASS_NAME,
                                                          "woocommerce-product-details__short-description")
                description = description_element.text
            except Exception as e:
                LOGGER.info("Error occurred while extracting description information:", e)
                description = None

            try:
                address = re.search(r'https?://\S+', description).group()
            except Exception as e:
                LOGGER.info("No address found")
                address = None

            if "k" in subscribed_number.replace("Followers", ""):
                follower = humanfriendly.parse_size(subscribed_number.replace("Followers", ""))
            elif "m" in subscribed_number.replace("Followers", ""):
                follower = humanfriendly.parse_size(subscribed_number.replace("Followers", ""))
            else:
                follower = int(subscribed_number.replace("Followers", ""))

            social_media = "Instagram"
            try:
                entry_data = {
                    "url": URL,
                    "title": name,
                    "category": categorie,
                    "price": price,
                    "social_media": social_media,
                    "social_media_address": address,
                    "followers": follower,
                    "offers_pending": offers,
                    "stock": stock,
                    "description": description
                }
                collection.insert_one(entry_data)
            except:
                LOGGER.info("Error Occured")

            driver.close()
            driver.switch_to.window(original_window_2)
            sleep(2)

        try:
            pagination_nav = driver.find_element(By.LINK_TEXT,"→")
            driver.execute_script("arguments[0].scrollIntoView();", pagination_nav)
            pagination_nav.click()
        except Exception as e:
            LOGGER.info(e)
            break

    driver.close()
    driver.switch_to.window(original_window)
    sleep(2)

client.close()
LOGGER.info("Connection Closed")
driver.quit()
LOGGER.info("Web Scraping finished")