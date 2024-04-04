
"""
	Usage
	-------------
	$ venv/bin/python3 -m scripts.accs_market --conf=$(pwd)/local.config.yaml
"""

import os
import json
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

# Limits crawling depth for a debug run
DEBUG = False

# Define a dictionary to map social media platforms to URLs
social_media_urls = {
	"Twitter": "https://accs-market.com/twitter",
	"Instagram": "https://accs-market.com/in",
	"Youtube": "https://accs-market.com/youtube",
	"Facebook": "https://accs-market.com/fb",
	"Tiktok": "https://accs-market.com/tiktok"
}

# Function to scrape data for a given social media platform URL
def scrape_data(driver, url, platform):
	
	outputs = []
	global DEBUG
	
	driver = driverModule.navigate(driver, url)
	if not driver:
		return False

	while True:
		elements = driver.find_elements(By.XPATH, "//div[@class='post__more']/a")

		for element in elements:
			link = element.get_attribute("href")
			URL = link
			original_window = driver.current_window_handle

			driver.switch_to.new_window('tab')
			driver = driverModule.navigate(driver, link)
			# sleep(5)
			for handle in driver.window_handles:
				if handle != original_window:
					driver.switch_to.window(handle)
					break
			sleep(5)

			## limit crawling depth for debugging purposes
			if DEBUG:
				if len(outputs) == 2:
					return outputs

			email_included = "none"
			promotion = "none"
			source_expense = "none"
			source_income = "none"
			supports = "none"
			content = "none"
			monetization_enabled = "none"

			try:
				group_data_div = driver.find_element(By.CLASS_NAME, "group-data")
				paragraphs = group_data_div.find_elements(By.TAG_NAME, "p")
				for paragraph in paragraphs:
					text = paragraph.text
					if 'Original' in text:
						email_included = text.split(":")[-1].strip()
					elif 'Ways' in text:
						promotion = text.split(":")[-1].strip()
					elif 'expense' in text:
						source_expense = text.split(":")[-1].strip()
					elif 'income' in text:
						source_income = text.split(":")[-1].strip()
					elif 'support' in text:
						supports = text.split(":")[-1].strip()
					elif 'Content' in text:
						content = text.split(":")[-1].strip()
					elif 'Monetization ' in text:
						monetization_enabled = text.split(":")[-1].strip()
			except Exception as e:
				LOGGER.info("Error occurred while extracting group data:", e)

			try:
				seller_name_div = driver.find_element(By.CLASS_NAME, "right-top__name")
				seller_element = seller_name_div.find_element(By.CLASS_NAME, "bold")
				seller = seller_element.text
			except Exception as e:
				LOGGER.info("Error occurred while extracting seller data:", e)
				seller = None

			try:
				names_element = driver.find_element("xpath",
													"/html/body/main/div/div/div[@class = 'group-info group']/div[@class = 'group-info']/h1/span")
				name = names_element.text
			except Exception as e:
				LOGGER.info("Error occurred while extracting names data:", e)
				name = None

			try:
				categoryAndAddress_element = driver.find_element("xpath",
																 "/html/body/main/div/div/div[3]/div[2]/p")
				splitCandA = categoryAndAddress_element.text.split('|')
				categorie = splitCandA[0].strip()
				address = splitCandA[1].strip()
			except Exception as e:
				LOGGER.info("Error occurred while extracting category and address data:", e)
				categorie = None
				address = None

			try:
				subscribed_element = driver.find_element("xpath",
														 "/html/body/main/div/div/div[3]/div[2]/div[1]/p[1]")
				subSplit = subscribed_element.text.split('-')
				follower = int(re.sub(r'\D', '', subSplit[0].strip()))
			except Exception as e:
				LOGGER.info("Error occurred while extracting subscribed data:", e)
				follower = None

			try:
				price_element = driver.find_element("xpath",
													"/html/body/main/div/div/div[3]/div[2]/div[2]")
				price = float(price_element.text.replace("$", "").replace(" ", ""))
			except Exception as e:
				LOGGER.info("Error occurred while extracting price data:", e)
				price = None

			try:
				listed_date_element = driver.find_element("xpath",
														  "/html/body/main/div/div/div[2]/span[1]")
				listedSplit = listed_date_element.text.split(":")
				listed_date = listedSplit[1].strip()
			except Exception as e:
				LOGGER.info("Error occurred while extracting listed date data:", e)
				listed_date = None

			try:
				views_element = driver.find_element("xpath", "/html/body/main/div/div/div[2]/span[3]")
				viewsSplit = views_element.text.split(":")
				view = int(viewsSplit[1].strip())
			except Exception as e:
				LOGGER.info("Error occurred while extracting views data:", e)
				view = None

			try:
				description_element = driver.find_element("xpath",
														  "/html/body/main/div/div/div[4]/div/div[1]/p[2]")
				description = description_element.text
			except Exception as e:
				LOGGER.info("Error occurred while extracting description data:", e)
				description = None

			try:
				monthly_income_element = driver.find_element("xpath",
															 "/html/body/main/div/div/div[3]/div[2]/div[1]/p[2]")
				monthly_expense_element = driver.find_element("xpath",
															  "/html/body/main/div/div/div[3]/div[2]/div[1]/p[3]")
				expensesSplit = monthly_expense_element.text.split("-")
				monthly_expense = float(re.search(r'\d+', expensesSplit[0].strip()).group())
				incomeSplit = monthly_income_element.text.split("-")
				monthly_income = float(re.search(r'\d+', incomeSplit[0].strip()).group())
			except Exception as e:
				LOGGER.info("Error occurred while extracting monthly income and expense data:", e)
				monthly_expense = None
				monthly_income = None

			social_media = platform

			try:
				if social_media == "Twitter" or social_media == "Instagram" or social_media == "Facebook":
					entry_data = {
						"url": URL,
						"title": name,
						"seller": seller,
						"listed_date": listed_date,
						"price": price,
						"social_media": social_media,
						"views": view,
						"description": description,
						"followers": follower,
						"category": categorie,
						"social_media_address": address,
						"monthly_income": monthly_income,
						"monthly_expense": monthly_expense,
						"email_included": email_included,
						"promotions": promotion,
						"source_expense": source_expense,
						"source_income": source_income,
						"support_account": supports,
						"content": content
					}
				else:
					entry_data = {
						"url": URL,
						"title": name,
						"seller": seller,
						"listed_date": listed_date,
						"price": price,
						"social_media": social_media,
						"views": view,
						"description": description,
						"followers": follower,
						"category": categorie,
						"social_media_address": address,
						"monthly_income": monthly_income,
						"monthly_expense": monthly_expense,
						"monetization_enabled": monetization_enabled,
						"promotions": promotion,
						"source_expense": source_expense,
						"source_income": source_income,
						"support_account": supports,
						"content": content
					}
				outputs.append(entry_data)

			except Exception as e:
				LOGGER.info("Error Occurred:", e)

			driver.close()
			driver.switch_to.window(original_window)
			sleep(7)
		try:
			next_page = driver.find_element(By.XPATH, "//div[@class='pagination']/a[@class='next']")
			next_page.click()
		except:
			break

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
				global DEBUG
				DEBUG = True
				
	LOGGER.info("spawn selenium instance.")
	driver = driverModule.get_new_browser_instance(config)


	platforms = ["Twitter", "Instagram", "Youtube","Facebook", "Tiktok"]
	for platform in platforms:
		if platform in social_media_urls:
			LOGGER.info(f'[accs_market] started scraping {platform}')

			filename = "accs_market_" + str(platform).lower() + "_" + utilityModule.get_timestamp() + '.json'
			output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)
			data = scrape_data(driver, social_media_urls[platform], platform)
			LOGGER.info(f'[accs_market] finished scraping {platform}')
			utilityModule.save_json_output(output_file, data)
			LOGGER.info("saved all records with length: %s"%str(len(data)))

	driverModule.close(driver)

if __name__ == "__main__":
	main()
