from hashlib import new
from telnetlib import EC
import re

from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from time import sleep

driver = Driver(uc=True)
client = MongoClient()
db = client.WebScraping
collection = db.WebScraping

website = "https://socialtradia.com/product-categories/"  # Categories
xpath_expressions = [
    "/html/body/div/div[1]/div/div[2]/div/div[2]/div/div/div/ul/li/div[2]/div/div[@class='nm-shop-loop-price']/span/del/span/span",
    "/html/body/div/div[1]/div/div[2]/div/div[2]/div/div/div/ul/li/div[2]/div/div[@class='nm-shop-loop-price']/span/span/span"
]

driver.get(website)

number_of_categories = driver.find_elements(By.XPATH, "//div[1]/div/div[1]/div[3]/div/div[@class='nm_column col-sm-4 mt-4']/a")

for categories in number_of_categories:

    categories_link = categories.get_attribute("href")
    original_window = driver.current_window_handle

    driver.switch_to.new_window('tab')
    driver.get(categories_link)
    sleep(2)
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break
    sleep(5)

    while True:

        try:
            names_elements = driver.find_elements(By.XPATH,
                                                  "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/ul/li/div/h3/a")
        except Exception as e:
            print("Error occurred while extracting list information:", e)

        try:
            category_element = driver.find_element(By.XPATH,
                                                   "/html/body/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/h1/span")
        except Exception as e:
            print("Error occurred while extracting category information:", e)

        try:
            price_element = driver.find_element(By.CLASS_NAME, "woocommerce-Price-amount")
        except Exception as e:
            print("Error occurred while extracting price information:", e)

        for name_element in names_elements:
            # Extract the text content from the name element
            name_and_followers = name_element.text.split("(")

            name = name_and_followers[0].strip()
            subscribed_number = name_and_followers[1].split(")")[0].strip()

            URL = name_element.get_attribute('href')
            categoriesList = category_element.text
            follower = subscribed_number
            price = price_element.text
            address = name
            social_media = "Instagram"
            try:
                entry_data = {
                    "url": URL,
                    "title": address,
                    "category": categoriesList,
                    "price": price,
                    "social_media": social_media,
                    "social_media_address": address,
                    "followers": follower
                }
                collection.insert_one(entry_data)
            except:
                print("Error Occured")

        sleep(10)

        try:
            pagination_nav = driver.find_element(By.LINK_TEXT,"→")
            driver.execute_script("arguments[0].scrollIntoView();", pagination_nav)
            pagination_nav.click()
        except Exception as e:
            print(e)
            break

    driver.close()
    driver.switch_to.window(original_window)
    sleep(2)

client.close()
print("Connection Closed")
driver.quit()
print("Web Scraping finished")