"""
	Usage
	-------------
	$ venv/bin/python3 -m scripts.fameseller_login --conf=$(pwd)/local.config.yaml
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




def scrape_data(driver, url, social_media):
	
	data = []
	global DEBUG
	LOGGER.info(f"DEBUG: {DEBUG == True}")  

	# login
	login = "https://fameseller.com/"
	driver.get(login)
	time.sleep(50)
	
	# index page
	driver = driverModule.navigate(driver, url)

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

			## limit crawling depth for debugging purposes
			if DEBUG:
				if len(outputs) == 2:
					return outputs

			try:
				title = driver.find_element(By.XPATH, "//h4").text
			except Exception as e:
				LOGGER.info("Error finding title:")
				LOGGER.error(e)
				title = None

			try:
				seller = driver.find_element(By.XPATH,
											 '//h5[@class="margin-bottom-15 f-size-24 slippa-semiblod"]/a[2]').text
			except Exception as e:
				LOGGER.info("Error finding seller:")
				LOGGER.error(e)
				seller = None

			try:
				seller_link = driver.find_element(By.XPATH,
												  '//h5[@class="margin-bottom-15 f-size-24 slippa-semiblod"]/a[2]').get_attribute(
					"href")
			except Exception as e:
				LOGGER.info("Error finding seller link:")
				LOGGER.error(e)
				seller_link = None

			try:
				social_media_link = driver.find_element(By.XPATH, '//h4/a').get_attribute("href")
			except Exception as e:
				LOGGER.info("Error finding seller:")
				LOGGER.error(e)
				social_media_link = None

			try:
				info_element = driver.find_elements(By.XPATH, "//div[@class='row margin-top-50']/div")
				age_element = info_element[0].text.split('\n')
				age = age_element[0]
				subscribers_element = info_element[2].text.split('\n')
				subscribers = subscribers_element[0].replace(',', '')
			except Exception as e:
				LOGGER.info("Error finding info:")
				LOGGER.error(e)
				age = None
				subscribers = None

			try:
				extra_info = driver.find_elements(By.XPATH, "//div[@class='domains-overview-inner']/ul/a/li/h5")
				net_profit = extra_info[1].text.replace('$', '').replace(',', '').strip()
				views = extra_info[2].text.replace(',', '')
			except Exception as e:
				LOGGER.info("Error finding extra info:")
				LOGGER.error(e)
				net_profit = None
				views = None

			try:
				price_element = driver.find_element(By.XPATH,
													"//a[@class = 'button ripple-effect move-on-hover full-width margin-top-20']/span").text.split(
					'$')
				price = price_element[-1].replace(',', '')
			except Exception as e:
				LOGGER.info("Error finding offers:")
				LOGGER.error(e)
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
				data.append(entry_data)
			except Exception as e:
				LOGGER.info("Error occurred:")
				LOGGER.error(e)

			driver.close()
			driver.switch_to.window(original_window)
			time.sleep(20)

		try:
			script = get_next_page()
			driver.execute_script(script)
			time.sleep(7)
		except Exception as e:
			LOGGER.warning("NextPage error")
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


	filename = "fameseller_" + utilityModule.get_timestamp() + '.json'
	output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)

	LOGGER.info("spawn selenium instance.")
	driver = driverModule.get_new_browser_instance(config)

	for platform in social_media_urls:
		LOGGER.info(f'[fameseller] started scraping {platform}')
		filename = "fameseller_" + str(platform).lower() + "_" + utilityModule.get_timestamp() + '.json'
		output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)
		data = scrape_data(driver, social_media_urls[platform], platform)
		LOGGER.info(f'[fameseller] finished scraping {platform}')
		utilityModule.save_json_output(output_file, data)
		LOGGER.info("saved all records with length: %s"%str(len(data)))

if __name__ == "__main__":
	main()
