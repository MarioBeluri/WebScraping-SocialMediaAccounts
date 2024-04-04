"""
    Usage
    -------------
    $ venv/bin/python3 -m scripts.instasale_login --conf=$(pwd)/local.config.yaml
"""

import os
import json
import sys
import re
import argparse
import time
import utils.io as IOModule
import utils.driver as driverModule
import utils.utility as utilityModule
import constants as constantsModule
from utils.logging import logger as LOGGER
from selenium.webdriver.common.by import By
from time import sleep

# limits crawling depth for a debug run
DEBUG = False


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


def main():

    global DEBUG
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
                DEBUG = True

    LOGGER.info(f"DEBUG: {DEBUG == True}")  

    filename = "instasale" + utilityModule.get_timestamp() + '.json'
    output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)

    LOGGER.info("spawn selenium instance.")
    driver = driverModule.get_new_browser_instance(config)

    data = []
    website_url = "https://insta-sale.com/listings/"
    login_url = "https://insta-sale.com/login/"

    driver.get(login_url)
    sleep(50)
    driver = driverModule.navigate(driver, website_url)

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

            ## limit crawling depth for debugging purposes
            if DEBUG:
                if len(outputs) == 2:
                    return outputs

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
    # end loop
        
    utilityModule.save_json_output(output_file, data)
    LOGGER.info("saved all records with length: %s"%str(len(data)))
    driver.close()


if __name__ == "__main__":
    main()
