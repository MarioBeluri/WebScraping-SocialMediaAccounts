from hashlib import new
from telnetlib import EC

from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from utils.logging import logger as LOGGER
from pymongo import MongoClient
from time import sleep


def get_next_page():
    """
    script to navigate to next page
    """
    script = """
    var nextLink = document.querySelector('a.next.page-numbers');
    var nextPageURL = nextLink.getAttribute('href');
    window.location.href = nextPageURL;
    """
    return script


driver = Driver(uc=True)
client = MongoClient()
db = client.WebScraping
collection = db.InstaSale
website = "https://insta-sale.com/listings/"
login = "https://insta-sale.com/login/"

driver.get(login)
sleep(20)
driver.get(website)
sleep(5)

while True:
    elements = driver.find_elements(By.XPATH, "/html/body/section[1]/div/div[2]/div[1]/div/a")

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
            username_element = driver.find_element("xpath",
                                                   "//div[@class = 'float-right']/h3")
            username = username_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting username information:", e)
            username = None

        try:
            category_element = driver.find_element(By.CLASS_NAME,
                                                   "title")
            categorie = category_element.text.split("Instagram")[0].strip()
        except Exception as e:
            LOGGER.info("Error occurred while extracting category information:", e)
            categorie = None

        try:
            likes_element = driver.find_element(By.XPATH,
                                                "//div[2]/div[1]/div/div[6]/div/h3")
            likes = int(likes_element.text.strip().replace(",", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting followers information:", e)
            follower = None

        try:
            followers_element = driver.find_element(By.XPATH,
                                                    "//div[2]/div[1]/div/div[2]/div/h3/span")
            follower = int(followers_element.text.strip().replace(",", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting followers information:", e)
            follower = None

        try:
            price_element = driver.find_element("xpath",
                                                "//div/div[3]/div/h3/span")
            price = float(price_element.text.strip().replace(",", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting price information:", e)
            price = None

        try:
            posts_element = driver.find_element("xpath",
                                                "//div[2]/div[1]/div/div[5]/div/h3/span")
            posts = int(posts_element.text)
        except Exception as e:
            LOGGER.info("Error occurred while extracting posts information:", e)
            posts = None

        try:
            elements_with_m_b_10 = driver.find_elements(By.CLASS_NAME, "m-b-10")
            description_paragraphs = elements_with_m_b_10[1].find_elements(By.TAG_NAME, "p")
            description = ""
            for paragraph in description_paragraphs:
                description += paragraph.text + "\n"
        except Exception as e:
            LOGGER.info("Error occurred while extracting description information:", e)
            description = None

        try:
            seller_info_element = driver.find_element(By.CLASS_NAME,
                                                      "wid-u-info")
            seller_element = seller_info_element.find_element(By.TAG_NAME, "h5")
            seller_name_element = seller_element.find_element(By.TAG_NAME, "a")
            seller_name = seller_name_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting seller name information:", e)
            seller_name = None

        try:
            seller_link = seller_name_element.get_attribute("href")
        except Exception as e:
            LOGGER.info("Error occurred while extracting seller link information:", e)
            seller_name = None

        try:
            last_online_element = seller_info_element.find_element(By.TAG_NAME, "h6")
            if last_online_element.text == "Online":
                last_online = last_online_element.text
            else:
                last_online = last_online_element.text.split(": ")[1]
        except Exception as e:
            LOGGER.info("Error occurred while extracting last online information:", e)
            last_online = None

        try:
            successful_trans_element = seller_info_element.find_element(By.CLASS_NAME, "escrow-count")
            successful_trans = int(successful_trans_element.text.split()[0])
        except Exception as e:
            LOGGER.info("Error occurred while extracting successful transactions number information:", e)
            successful_trans = None

        social_media = "Instagram"

        try:
            entry_data = {
                "url": URL,
                "title": username,
                "price": price,
                "social_media": social_media,
                "description": description,
                "followers": follower,
                "category": categorie,
                "likes": likes,
                "posts": posts,
                "seller_name": seller_name,
                "seller_link": seller_link,
                "last_online": last_online,
                "successful_transactions": successful_trans
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
        script = get_next_page()
        driver.execute_script(script)
    except:
        break

client.close()
LOGGER.info("Connection Closed")
driver.quit()
LOGGER.info("Web Scraping finished")