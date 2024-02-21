"""
	Copyright (C) 2024  Soheil Khodayari, CISPA
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.
	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.


	Description:
	-------------
	Data scraper for https://www.toofame.com

	Catalogs
	-------------
	- Instagram: https://www.toofame.com/instagram-accounts-for-sale/

	Usage
	-------------
	$ python3 toofame_scrape.py --conf=$(pwd)/local.config.yaml

	
"""
import os
import json
import argparse
import time
import utils.io as IOModule
import utils.driver as driverModule
import constants as constantsModule
from utils.logging import logger as LOGGER


def get_data_script_for_catalog(batch_no, batch_size=18):
	"""
	script to collect account info from the listing catalog of instagram accounts
	"""
	script = """
	var offset = parseInt(%d) * parseInt(%d);
	var card_items = document.getElementsByClassName('proitem');
	var data = [];
	for (var i=offset; i< card_items.length; i++){
		var item = card_items[i];
		var e = {};
		e.sale_percent = item.querySelector("[class=sale_percent").innerText.trim();
		e.shopurl = item.querySelector("a[class=pro_image").getAttribute("href").trim();
		e.imageurl = item.querySelector("span[class=ifront] > img").getAttribute('src').trim();
		e.title = item.querySelector("a[class=pro_title").innerText.trim();

		var prices = item.querySelector("div[class=pro_price").innerText.trim().split('\\n');
		e.price = prices[0];
		e.discounted = prices[1];
		data.push(e);
	}
	return data;
	"""%(batch_no, batch_size)

	return script

def get_data_script_for_item():
	"""
	script to collect additional info for each account
	"""

	# example:
	# 'Followers: 309,475\nAverage Likes: 93,618\nUsername: parkourss'
	
	script = """
	var qs = document.querySelector('div[class=woocommerce-product-details__short-description] > p').innerText.trim();
	var parts = qs.split('\\n');
	
	var s = {};
	s.followers = "";
	s.likes = "";
	s.username = "";
	s.accounturl = "";

	if(parts.length >= 2){
		var followers = parts[0].replace('Followers:', '').trim();
		var likes = parts[1].replace('Average Likes:', '').trim();
		var username = parts[2].replace('Username:', '').trim();
		var accounturl = document.querySelector('div[class=woocommerce-product-details__short-description] > p > a').getAttribute('href');
	
		s.followers = followers;
		s.likes = likes;
		s.username = username;
		s.accounturl = accounturl;
	}
	return s;
	"""
	return script

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


	driver = driverModule.get_new_browser_instance(config)

	# init data scraping
	catalog_url = "https://www.toofame.com/instagram-accounts-for-sale/"


	driver = driverModule.navigate(driver, catalog_url)
	main_window = driver.current_window_handle

	# create a new tab and return
	driver.switch_to.new_window('tab')
	driver.get('https://google.com')
	driver.switch_to.window(main_window)
	time.sleep(5)

	data = []
	batch_size = 18
	batch_no = 0
	MAX_ITERATIONS = 2
	done = False

	batch_script = get_data_script_for_catalog(batch_no, batch_size)

	while not done:
		batch_script = get_data_script_for_catalog(batch_no, batch_size)
		batch_data = driver.execute_script(batch_script)
		if batch_no < MAX_ITERATIONS and len(batch_data) > batch_no*batch_size:
			
			completed_batch_data = []
			driver.switch_to.window(driver.window_handles[1])

			for item in batch_data:
				if "shopurl" in item:
					shopurl = item["shopurl"]
					driver = driverModule.navigate(driver, shopurl)	

					item_script = get_data_script_for_item()
					item_data = driver.execute_script(item_script)

					item["followers"] = item_data["followers"]
					item["likes"] = item_data["likes"]
					item["username"] = item_data["username"]
					item["accounturl"] = item_data["accounturl"]
					completed_batch_data.append(item)

			data.extend(completed_batch_data)
			batch_no += 1

			driver.switch_to.window(driver.window_handles[0])
			# press the load more button
			driver.execute_script("document.getElementById('load-more').click()")

		else:
			LOGGER.info(f"batch_no: ${batch_no}; length: ${len(batch_data)}")
			done = True
			break

	driverModule.close(driver)

	SITE_NAME = "toofame"
	output_file = os.path.join(constantsModule.OUTPUT_DIR, SITE_NAME + ".json")
	with open(output_file, 'w+', encoding='utf-8') as fd:
		json.dump(data, fd, ensure_ascii=False, indent=4)


if __name__ == "__main__":
	main()


