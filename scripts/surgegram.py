"""
	Usage
	-------------
	$ venv/bin/python3 -m scripts.surgegram --conf=$(pwd)/local.config.yaml
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


	filename = "surgegram_" + utilityModule.get_timestamp() + '.json'
	output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)

	data = []
	pattern = r'(\d+K)\s(.+?)\sInstagram'

	LOGGER.info("spawn selenium instance.")
	driver = driverModule.get_new_browser_instance(config)

	website_url =  "https://www.surgegram.com/accounts/"
	LOGGER.info(f'[surgegram] started scraping')
	driver = driverModule.navigate(driver, website_url)


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

			if DEBUG:
				if len(data) == 2:
					break
			try:
				username_element = driver.find_element("xpath",
													   "//h1")
				username = username_element.text
			except Exception as e:
				LOGGER.info("Error occurred while extracting username information:")
				LOGGER.error(e)
				username = None

			try:
				matches = re.findall(pattern, username)
				if matches:
					categorie = matches[0][1]
				else:
					print("No category match found.")
					categorie = None
			except Exception as e:
				LOGGER.info("Error occurred while extracting category information:")
				LOGGER.error(e)
				categorie = None

			try:
				likes_script = get_likes()
				likes_data = driver.execute_script(likes_script)
				likes = likes_data[-1].split(" ")[0].replace(",", "")
			except Exception as e:
				LOGGER.info("Error occurred while extracting likes information:")
				LOGGER.error(e)
				likes = None

			try:
				price_element = driver.find_elements("xpath",
													 "//div[@class = 'product-info summary col-fit col entry-summary product-summary text-left']/div[@class ='price-wrapper']//span[@class = 'woocommerce-Price-amount amount']/bdi")
				if len(price_element) > 2:
					price = price_element[1].text.replace("$", "").replace(",", "")
				else:
					price = price_element[0].text.replace("$", "").replace(",", "")
			except Exception as e:
				LOGGER.info("Error occurred while extracting price information:")
				LOGGER.error(e)
				price = None

			try:
				users_script = get_users()
				users_data = driver.execute_script(users_script)
				users = users_data[-1].split(" ")[0].replace(",", "")
			except Exception as e:
				LOGGER.info("Error occurred while extracting users information:")
				LOGGER.error(e)
				users = None

			try:
				description_element = driver.find_element(By.XPATH, "//span[@style='color: #555555;']")
				description = description_element.text
			except Exception as e:
				LOGGER.info("Error occurred while extracting description information:")
				LOGGER.error(e)
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
				data.append(entry_data)

			except Exception as e:
				LOGGER.warning("Error occurred:")
				LOGGER.error(e)

			driver.close()
			driver.switch_to.window(original_window)
			sleep(2)

		try:
			nextPage = driver.find_element(By.XPATH, '//a[@class="next page-number"]')
			nextPage.click()
		except:
			break

	LOGGER.info(f'[surgegram] finished scraping')
	utilityModule.save_json_output(output_file, data)
	LOGGER.info("saved all records with length: %s"%str(len(data)))
	driver.close()

if __name__ == "__main__":
	main()