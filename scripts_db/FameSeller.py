import time
from hashlib import new
from telnetlib import EC

from pymongo import MongoClient
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from utils.logging import logger as LOGGER

social_media_urls = {
    "Twitter": "https://fameseller.com/main/category/buy-twitter-accounts",
    "Instagram": "https://fameseller.com/main/category/buy-instagram-accounts",
    "Facebook": "https://fameseller.com/main/category/buy-facebook-pages-groups",
    "Youtube": "https://fameseller.com/main/category/buy-youtube-channels",
    "Tiktok": "https://fameseller.com/main/category/buy-tiktok-accounts"
}


def get_next_page():
    """
    script to navigate to next page
    """
    script = """
    var nextLink = document.querySelector('.pagination-arrow a[rel="next"]');
    nextLink.click();
    """
    return script


def scrape_data(driver, url, social_media, collection):
    login = "https://fameseller.com/"
    driver.get(login)
    time.sleep(50)
    driver.get(url)
    time.sleep(5)

    while True:

        elements = driver.find_elements("xpath", "//div[@class = 'listings-container grid-layout margin-top-35']/div/a")

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
                title = driver.find_element(By.XPATH, "//h4").text
            except Exception as e:
                LOGGER.info("Error finding title:", e)
                title = None

            try:
                seller = driver.find_element(By.XPATH,
                                             '//h5[@class="margin-bottom-15 f-size-24 slippa-semiblod"]/a[2]').text
            except Exception as e:
                LOGGER.info("Error finding seller:", e)
                seller = None

            try:
                seller_link = driver.find_element(By.XPATH,
                                                  '//h5[@class="margin-bottom-15 f-size-24 slippa-semiblod"]/a[2]').get_attribute(
                    "href")
            except Exception as e:
                LOGGER.info("Error finding seller link:", e)
                seller_link = None

            try:
                social_media_link = driver.find_element(By.XPATH, '//h4/a').get_attribute("href")
            except Exception as e:
                LOGGER.info("Error finding seller:", e)
                social_media_link = None

            try:
                info_element = driver.find_elements(By.XPATH, "//div[@class='row margin-top-50']/div")
                age_element = info_element[0].text.split('\n')
                age = age_element[0]
                subscribers_element = info_element[2].text.split('\n')
                subscribers = int(subscribers_element[0].replace(',', ''))
            except Exception as e:
                LOGGER.info("Error finding info:", e)
                age = None
                subscribers = None

            try:
                extra_info = driver.find_elements(By.XPATH, "//div[@class='domains-overview-inner']/ul/a/li/h5")
                net_profit = float(extra_info[1].text.replace('$', '').replace(',', '').strip())
                views = int(extra_info[2].text.replace(',', ''))
            except Exception as e:
                LOGGER.info("Error finding extra info:", e)
                net_profit = None
                views = None

            try:
                price_element = driver.find_element(By.XPATH,
                                                    "//a[@class = 'button ripple-effect move-on-hover full-width margin-top-20']/span").text.split(
                    '$')
                price = float(price_element[-1].replace(',', ''))
            except Exception as e:
                LOGGER.info("Error finding offers:", e)
                price = None

            social_medias = social_media

            try:
                entry_data = {
                    "url": URL,
                    "title": title,
                    "seller": seller,
                    "seller_link": seller_link,
                    "subscribers": subscribers,
                    "net_profit": net_profit,
                    "views": views,
                    "age": age,
                    "social_media_link": social_media_link,
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
social_media_input = input("Enter social media platform (Twitter, Instagram, Facebook, Tiktok, Youtube): ")

# Validate user input and scrape data accordingly
if social_media_input in social_media_urls:
    driver = Driver(uc=True, headed=True)
    client = MongoClient()
    db = client.WebScraping
    collection = db.FameSeller
    scrape_data(driver, social_media_urls[social_media_input], social_media_input, collection)
    client.close()
    LOGGER.info("Connection Closed")
    driver.quit()
    LOGGER.info("Web Scraping finished")
else:
    LOGGER.info("Invalid social media platform. Please enter a valid Social Media platform.")