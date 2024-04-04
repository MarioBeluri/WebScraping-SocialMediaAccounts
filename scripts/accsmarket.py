"""
	Usage
	-------------
	$ venv/bin/python3 -m scripts.accsmarket --conf=$(pwd)/local.config.yaml
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

DEBUG = False

social_media_urls = {
	"Twitter": "https://accsmarket.com/en/catalog/twitter",
	"Instagram": "https://accsmarket.com/en/catalog/instagram",
	"Facebook": "https://accsmarket.com/en/catalog/facebook"
}

def scrape_data(driver, url, social_media):
	
	outputs = []
	driver = driverModule.navigate(driver, url)
	listings = driver.find_elements(By.XPATH, "//div[@class = 'soc-text']/p/a")

	quantity = [quantity.text.split()[0] for quantity in driver.find_elements(By.XPATH, "//div[@class = 'soc-qty']")]
	URls = [url.get_attribute("href") for url in driver.find_elements(By.XPATH, "//div[@class = 'soc-text']/p/a")]
	prices = [price.get_attribute("textContent") for price in
			  driver.find_elements(By.XPATH, "//div[@class = 'soc-price']/div")]
	descriptions = [listing.get_attribute("text") for listing in listings]
	social_medias = [social_media for _ in range(len(listings))]

	for i in range(len(prices)):
		index_of_dollar = prices[i].find('$')
		if index_of_dollar != -1:
			prices[i] = prices[i][index_of_dollar:].strip().replace("$", "").replace(',', '.')

	try:
		for j in range(len(listings)):
			entry_data = {
				"url": URls[j],
				"title": descriptions[j],
				"quantity": int(quantity[j]),
				"price": float(prices[j]),
				"social_media": social_medias[j]
			}
			outputs.append(entry_data)
	except:
		err = sys.exc_info()[0]
		LOGGER.warning("error occured.")
		LOGGER.error(err)

	return outputs

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
				DEBUG = True

	LOGGER.info("spawn selenium instance.")
	driver = driverModule.get_new_browser_instance(config)

	for platform in social_media_urls:
		LOGGER.info(f'[accsmarket] started scraping {platform}')
		filename = "accsmarket_" + str(platform).lower() + "_" + utilityModule.get_timestamp() + '.json'
		output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)
		data = scrape_data(driver, social_media_urls[platform], platform)
		LOGGER.info(f'[accsmarket] finished scraping {platform}')
		utilityModule.save_json_output(output_file, data)
		LOGGER.info("saved all records with length: %s"%str(len(data)))

	driver.close()


if __name__ == "__main__":
	main()