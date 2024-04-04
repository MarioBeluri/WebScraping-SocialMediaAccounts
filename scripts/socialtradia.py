"""
	Usage
	-------------
	$ venv/bin/python3 -m scripts.socialtradia --conf=$(pwd)/local.config.yaml
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

	data = []

	filename = "socialtradia_" + utilityModule.get_timestamp() + '.json'
	output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)

	LOGGER.info("spawn selenium instance.")
	driver = driverModule.get_new_browser_instance(config)

	website_url =  "https://socialtradia.com/product-categories/"
	LOGGER.info(f'[surgegram] started scraping')
	driver = driverModule.navigate(driver, website_url)


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

		if DEBUG:
			if len(data) == 2:
				break
					
		while True:

			try:
				names_elements = driver.find_elements(By.XPATH,
													  "//div[@class = 'nm-shop-loop-details']/h3/a")
			except Exception as e:
				LOGGER.info("Error occurred while extracting list information:")
				LOGGER.error(e)

			try:
				category_element = driver.find_element(By.XPATH,
													   "/html/body/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/h1/span")
				categorie = category_element.text
			except Exception as e:
				LOGGER.info("Error occurred while extracting category information:")
				LOGGER.error(e)

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
					LOGGER.info("Error occurred while extracting name information:")
					LOGGER.error(e)
					name = "NotFound"
					subscribed_number = ""

				try:
					price_element = driver.find_element(By.CLASS_NAME, "woocommerce-Price-amount")
					price = price_element.text.replace("$", "").replace(",", "")
				except Exception as e:
					LOGGER.info("Error occurred while extracting price information:")
					LOGGER.error(e)
					price = ""

				try:
					offers_pending_element = driver.find_element(By.CLASS_NAME, "ofw-info")
					offers = offers_pending_element.text.split()[0]
				except Exception as e:
					LOGGER.info("Error occurred while extracting offer information:")
					LOGGER.error(e)
					offers = ""

				try:
					stock_element = driver.find_element(By.CLASS_NAME, "stock")
					stock = stock_element.text.split()[0]
				except Exception as e:
					LOGGER.info("Error occurred while extracting stock information:")
					LOGGER.error(e)
					stock = ""

				try:
					description_element = driver.find_element(By.CLASS_NAME,
															  "woocommerce-product-details__short-description")
					description = description_element.text
				except Exception as e:
					LOGGER.info("Error occurred while extracting description information:")
					LOGGER.error(e)
					description = None

				try:
					address = re.search(r'https?://\S+', description).group()
				except Exception as e:
					LOGGER.info("No address found")
					address = None

				try:
					follower = subscribed_number.replace("Followers", "")
				except Exception as e:
					follower = ""

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
					data.append(entry_data)
				except:
					LOGGER.info("Error occured")

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
		# end while loop

	utilityModule.save_json_output(output_file, data)
	LOGGER.info("saved all records with length: %s"%str(len(data)))
	driver.close()

if __name__ == "__main__":
    main()