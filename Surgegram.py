from hashlib import new
from telnetlib import EC

import re
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from utils.logging import logger as LOGGER
from pymongo import MongoClient
from time import sleep


def get_likes():
    """
    Function to extract likes count from product-excerpt elements
    """
    script = """
    var elements = document.querySelectorAll('.product-excerpt');
    var likesData = [];
    for (var i = 0; i < elements.length; i++) {
        var textContent = elements[i].textContent;
        if (textContent.includes("Likes")) {
            likesData.push(textContent.trim()); // Pushing trimmed textContent to likesData array
        }
    }
    return likesData; // Returning array of textContent containing "Likes"
    """
    return script


def get_users():
    """
    Function to extract follower count from product-excerpt elements
    """
    script = """
    var elements = document.querySelectorAll('.product-excerpt');
    var followerData = [];
    for (var i = 0; i < elements.length; i++) {
        var textContent = elements[i].textContent;
        if (textContent.includes("Users")) {
            followerData.push(textContent.trim()); // Pushing trimmed textContent to followerData array
        }
    }
    return followerData; // Returning array of textContent containing "Users"
    """
    return script


pattern = r'(\d+K)\s(.+?)\sInstagram'
driver = Driver(uc=True)
client = MongoClient()
db = client.WebScraping
collection = db.Surgegram
website = "https://www.surgegram.com/accounts/"

driver.get(website)
sleep(3)

while True:
    elements = driver.find_elements(By.XPATH, "//div[@class='box-image']/div[@class = 'image-fade_in_back']/a")

    for element in elements:
        link = element.get_attribute("href")

        URL = link
        original_window = driver.current_window_handle

        driver.switch_to.new_window('tab')
        driver.get(link)
        sleep(3)
        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break
        sleep(3)

        try:
            username_element = driver.find_element("xpath",
                                                   "//h1")
            username = username_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting username information:", e)
            username = None

        try:
            matches = re.findall(pattern, username)
            if matches:
                categorie = matches[0][1]
            else:
                print("No category match found.")
                categorie = None
        except Exception as e:
            LOGGER.info("Error occurred while extracting category information:", e)
            categorie = None

        try:
            likes_script = get_likes()
            likes_data = driver.execute_script(likes_script)
            likes = int(likes_data[-1].split(" ")[0].replace(",", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting likes information:", e)
            likes = None

        try:
            price_element = driver.find_elements("xpath",
                                                 "//div[@class = 'product-info summary col-fit col entry-summary product-summary text-left']/div[@class ='price-wrapper']//span[@class = 'woocommerce-Price-amount amount']/bdi")
            if len(price_element) > 2:
                price = float(price_element[1].text.replace("$", "").replace(",", ""))
            else:
                price = float(price_element[0].text.replace("$", "").replace(",", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting price information:", e)
            price = None

        try:
            users_script = get_users()
            users_data = driver.execute_script(users_script)
            users = int(users_data[-1].split(" ")[0].replace(",", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting users information:", e)
            users = None

        try:
            description_element = driver.find_element(By.XPATH, "//span[@style='color: #555555;']")
            description = description_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting description information:", e)
            description = None

        social_media = "Instagram"

        try:
            entry_data = {
                "url": URL,
                "title": username,
                "price": price,
                "social_media": social_media,
                "description": description,
                "followers": users,
                "category": categorie,
                "likes": likes,
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
        nextPage = driver.find_element(By.XPATH, '//a[@class="next page-number"]')
        nextPage.click()
    except:
        break

client.close()
LOGGER.info("Connection Closed")
driver.quit()
LOGGER.info("Web Scraping finished")