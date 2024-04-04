"""
    Usage
    -------------
    $ venv/bin/python3 -m scripts.midman --conf=$(pwd)/local.config.yaml
    
    TODO: fix runtime errors

"""

import os
import json
import sys
import re
import argparse
import time
import humanfriendly
import utils.io as IOModule
import utils.driver as driverModule
import utils.utility as utilityModule
import constants as constantsModule
from utils.logging import logger as LOGGER
from selenium.webdriver.common.by import By
from time import sleep

# limits crawling depth for a debug run
DEBUG = False

social_media_urls = {
    "Twitter": "https://mid-man.com/twitter/",
    "Instagram": "https://mid-man.com/instagram/",
    "Youtube": "https://mid-man.com/youtube/",
    "Facebook": "https://mid-man.com/facebook/",
    "Tiktok": "https://mid-man.com/tiktok/"
}

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

def scrape_data(driver, url, socialMedia):
    
    data = [] # outputs
    driver = driverModule.navigate(driver, url)
    # driver.maximize_window()
    global DEBUG
    LOGGER.info(f"DEBUG: {DEBUG == True}")    

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
            if DEBUG:
                if len(data) == 2:
                    return data
            try:
                followerandCategory_element = driver.find_element(By.CLASS_NAME, "list-meta").find_elements(By.TAG_NAME, "span")
                follower_count = followerandCategory_element[0].text.split()[0]
                if "K" in follower_count:
                    follower = humanfriendly.parse_size(follower_count)
                elif "M" in follower_count:
                    follower = humanfriendly.parse_size(follower_count)
                else:
                    follower = int(follower_count)
            except Exception as e:
                LOGGER.info("Error occurred while extracting follower data:", e)
                follower = None

            try:
                categorie = followerandCategory_element[1].text
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
               data.append(entry_data)
            except Exception as e:
                LOGGER.info("Error occurred:", e)

            driver.close()
            driver.switch_to.window(original_window)
            sleep(2)
        try:
            script = get_next_page()
            driver.execute_script(script)
        except:
            break

    return data

def main():

    CONFIG_FILE_DEFAULT = os.path.join(constantsModule.BASE_DIR, 'config.yaml')
    p = argparse.ArgumentParser(description='This script runs the scraper.')
    p.add_argument('--conf', "-C",
                    metavar="FILE",
                    default=CONFIG_FILE_DEFAULT,
                    help='configuration file. (default: %(default)s)',
                    type=str)

    args= vars(p.parse_args())
    config = IOModule.load_config_yaml(args["conf"])

    if "env" in config:
        if "output_dir" in config["env"]:
            constantsModule.OUTPUT_DIR = config["env"]["output_dir"]

        if "debug" in config["env"]:
            d = str(config["env"]["debug"]).lower()
            if d == "true":
                global DEBUG
                DEBUG = True

    LOGGER.info("spawn selenium instance.")
    driver = driverModule.get_new_browser_instance(config)

    for platform in social_media_urls:
        LOGGER.info(f'[midman] started scraping {platform}')
        filename = "midman_" + str(platform).lower() + "_" + utilityModule.get_timestamp() + '.json'
        output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)
        data = scrape_data(driver, social_media_urls[platform], platform)
        LOGGER.info(f'[midman] finished scraping {platform}')
        utilityModule.save_json_output(output_file, data)
        LOGGER.info("saved all records with length: %s"%str(len(data)))

    driver.close()


if __name__ == "__main__":
    main()