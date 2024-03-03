from hashlib import new
from telnetlib import EC

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from time import sleep
import humanfriendly
from utils.logging import logger as LOGGER

social_media_urls = {
    "Twitter": "https://mid-man.com/twitter/",
    "Instagram": "https://mid-man.com/instagram/",
    "Youtube": "https://mid-man.com/youtube/",
    "Facebook": "https://mid-man.com/facebook/",
    "Tiktok": "https://mid-man.com/tiktok/"
}

def scrape_data(driver, url, socialMedia, collection):
    driver.get(url)
    sleep(10)

    while True:
        elements = driver.find_elements("xpath", "//div[@class = 'product-shop-area']/div/div/div/div/div/a")

        for element in elements:
            link = element.get_attribute("href")
            URL = link
            original_window = driver.current_window_handle

            driver.switch_to.new_window('tab')
            driver.get(link)
            sleep(5)
            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    break
            sleep(5)

            try:
                follower_element = driver.find_element(By.CLASS_NAME, "list-inline-item").find_element(By.TAG_NAME, "span")
                follower_count = follower_element.text.split()[0]
                if "K" in follower_count:
                    follower = humanfriendly.parse_size(follower_count)
                elif "M" in follower_count.text:
                    follower = humanfriendly.parse_size(follower_count)
                else:
                    follower = int(follower_count)
            except Exception as e:
                LOGGER.info("Error occurred while extracting follower data:", e)
                follower = None

            try:
                category_element = driver.find_element(By.CLASS_NAME, "list-inline-item:last-child").find_element(
                    By.TAG_NAME, "span")
                categorie = category_element.text
            except Exception as e:
                LOGGER.info("Error occurred while extracting category data:", e)
                categorie = None

            try:
                title_element = driver.find_element(By.CSS_SELECTOR, ".widget-title-product h1")
                title = title_element.text
            except Exception as e:
                LOGGER.info("Error occurred while extracting title data:", e)
                title = None

            try:
                price_element = driver.find_element(By.CLASS_NAME, "woocommerce-Price-amount")
                price_text = price_element.text
                price = float(price_text.split('$')[1].replace(",", ""))
            except Exception as e:
                LOGGER.info("Error occurred while extracting price data:", e)
                price = None

            try:
                author_element = driver.find_element(By.CLASS_NAME, "name-author").find_element(By.TAG_NAME, "a")
                seller = author_element.text
            except Exception as e:
                LOGGER.info("Error occurred while extracting seller data:", e)
                seller = None

            try:
                seller_website = author_element.get_attribute("href")
            except Exception as e:
                LOGGER.info("Error occurred while extracting seller website data:", e)
                seller_website = None

            try:
                description_element = driver.find_element(By.ID, "tab-description")
                description = description_element.text
            except Exception as e:
                LOGGER.info("Error occurred while extracting description data:", e)
                description = None

            social_media = socialMedia

            try:
               entry_data = {
                    "url": URL,
                    "title": title,
                    "seller": seller,
                    "price": price,
                    "social_media": social_media,
                    "description": description,
                    "followers": follower,
                    "category": categorie,
                    "seller_website": seller_website,
                }
               collection.insert_one(entry_data)
            except Exception as e:
                LOGGER.info("Error Occurred:", e)
                client.close()
                LOGGER.info("Connection Closed")

            driver.close()
            driver.switch_to.window(original_window)
            sleep(2)
        try:
            next_page = driver.find_element(By.XPATH, "//a[@class='next page-numbers']")
            next_page.click()
        except:
            break

# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, Facebook, Tiktok, Youtube): ")

# Validate user input and scrape data accordingly
if social_media_input in social_media_urls:
    driver = Driver(uc=True)
    client = MongoClient()
    db = client.WebScraping
    collection = db.MidMan
    scrape_data(driver, social_media_urls[social_media_input], social_media_input, collection)
    driver.quit()
    client.close()
    LOGGER.info("Connection Closed")
    LOGGER.info("Scraping finished")
else:
    LOGGER.info("Invalid social media platform. Please enter a valid Social Media platform.")
