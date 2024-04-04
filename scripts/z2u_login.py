"""
    Usage
    -------------
    $ venv/bin/python3 -m scripts.z2u_login --conf=$(pwd)/local.config.yaml
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


def scrape_data(driver, url, social_media):
    
    data = []
    global DEBUG
    LOGGER.info(f"DEBUG: {DEBUG == True}") 

    login = "https://www.z2u.com/"

    driver.get(login)
    time.sleep(50)

    # index page
    driver = driverModule.navigate(driver, url)

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

            ## limit crawling depth for debugging purposes
            if DEBUG:
                if len(outputs) == 2:
                    return outputs

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
                data.append(entry_data)
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
            LOGGER.error("Next Page error")
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


    filename = "z2u_" + utilityModule.get_timestamp() + '.json'
    output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)

    LOGGER.info("spawn selenium instance.")
    driver = driverModule.get_new_browser_instance(config)

    for platform in social_media_urls:
        LOGGER.info(f'[z2u] started scraping {platform}')
        filename = "z2u_" + str(platform).lower() + "_" + utilityModule.get_timestamp() + '.json'
        output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)
        data = scrape_data(driver, social_media_urls[platform], platform)
        LOGGER.info(f'[z2u] finished scraping {platform}')
        utilityModule.save_json_output(output_file, data)
        LOGGER.info("saved all records with length: %s"%str(len(data)))

if __name__ == "__main__":
    main()


