from hashlib import new
from telnetlib import EC

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from utils.logging import logger as LOGGER
from pymongo import MongoClient
from time import sleep

driver = Driver(uc=True)
client = MongoClient()
db = client.WebScraping
collection = db.SwapSocials
website = "https://swapsocials.com/instagram-accounts-for-sale/"

driver.get(website)

while True:
    elements = driver.find_elements("xpath", "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/ul/li/div[@class = 'nm-shop-loop-thumbnail nm-loader']/a")

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
            names_element = driver.find_element("xpath",
                                                "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[1]/h1")
            name = names_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting names information:", e)
            name = None

        try:
            category_element = driver.find_element("xpath",
                                                   "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div/div[1]/nav/a[3]")
            categorie = category_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting category information:", e)
            categorie = None

        try:
            subscribedAndAverageLikes_element = driver.find_element(By.XPATH,
                                                                    "//div[@class='woocommerce-product-details__short-description']//p[2]")
            subAndLikes = subscribedAndAverageLikes_element.text
            split_index = subAndLikes.index('\n')
            followers_string = subAndLikes[:split_index]
            likes_string = subAndLikes[split_index + 1:]
            followers_split = followers_string.split(":")
            follower = int(followers_split[1].strip())
            likes_split = likes_string.split(":")
            average_like = int(likes_split[1].strip())
        except Exception as e:
            LOGGER.info("Error occurred while extracting followers information:", e)
            follower = None
            average_like = None

        try:
            price_element = driver.find_elements("xpath",
                                                 "//p[@class='price']//span[@class='woocommerce-Price-amount amount']/bdi")
            price = float(price_element[0].text.replace("$", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting price information:", e)
            price = None

        try:
            description_element = driver.find_element("xpath",
                                                      "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/p[3]")
            description = description_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting description information:", e)
            description = None

        social_media = "Instagram"

        try:
            entry_data = {
                    "url": URL,
                    "title": name,
                    "price": price,
                    "social_media": social_media,
                    "description": description,
                    "followers": follower,
                    "category": categorie,
                    "average_likes": average_like,
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
        next_page = driver.find_element(By.XPATH,
                                        "//nav[@class='woocommerce-pagination nm-pagination nm-infload']//a[@class='next page-numbers']")
        next_page.click()
    except:
        break

client.close()
LOGGER.info("Connection Closed")
driver.quit()
LOGGER.info("Web Scraping finished")