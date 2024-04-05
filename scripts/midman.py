"""
	Usage
	-------------
	$ venv/bin/python3 -m scripts.midman --conf=$(pwd)/local.config.yaml

	Notes:
	-------------
	it seems that the site has anti-bot protection in headless mode!
	
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
	if(nextLink){
		var nextPageURL = nextLink.getAttribute('href');
		window.location.href = nextPageURL;
		return true;
	}
	return false;
	"""
	return script

def scrape_data(driver, url, platform):
	
	data = [] # outputs
	driver = driverModule.navigate(driver, url)
	# driver.maximize_window()
	global DEBUG
	LOGGER.info(f"DEBUG: {DEBUG == True}")    


	while True:
		script="""
		var items = [];
		var elements = document.getElementsByClassName('download-item-content')
		for(var e of elements){
		 	var o = {};
		 	
		 	let cat = e.querySelector('[class=product-topic]');
		 	if(cat){
		 		cat = cat.innerText.trim();
		 	}else{
		 		cat = ""
		 	}
		 	o.category = cat;

		 	let url = e.querySelector('[class=product-title]');
		 	if(url){
		 		url = url.getAttribute('href');
		 	}else{
		 		url = "";
		 	}
		 	o.url = url;

		 	let u = e.querySelector('[class=product-title]');
		 	if(u){
		 		u = u.innerText.trim();
		 	}else{
		 	 	u = ""
		 	}
		 	o.username_desc= u;

		 	if(u.includes(' ')){
		 		if(u.includes('@')){
		 			let s = u.slice(u.indexOf('@'))
		 			let at_index = s.indexOf('@');
		 			let space_index = s.indexOf(' ');
		 			s = s.substring(at_index, space_index);
		 			o.username = s.replace('@', '');
		 		}else{
		 		 	o.username= "";
		 		}
		 	}else{
		 		o.username = u.replace('@', '');
		 	}
		 	
		 	let followers = e.querySelector('.list-follow');
		 	if(followers){
		 		followers = followers.innerText.replace('followers', '').trim();
		 	}else{
		 		followers = "";
		 	}
		 	o.followers = followers;

		 	let price = e.querySelector('.price');
		 	if(price){
		 		price = price.innerText.trim();
		 	}else{
		 		price = "";
		 	}
		 	o.price = price;
		 	items.push(o);
		}
		return items
		"""
		records = driver.execute_script(script)
		data.extend(records)

		next_page = driver.execute_script(get_next_page())
		# break on last page
		if not next_page:
			break
		sleep(constantsModule.PAGE_LOAD_WAIT_TIME_DEFAULT)


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


	platforms = [
		"Twitter",
		"Instagram",
		"Youtube",
		"Facebook",
		"Tiktok"
	]

	for platform in platforms:
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