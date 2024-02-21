
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
	selenium driver for chrome
	
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from utils.logging import logger as LOGGER
import constants as constantsModule

def get_new_browser_instance(config):
	"""
	return a new chrome instance
	"""

	# note: must not contain `--disable-dev-shm-usage` for ramfs
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument("--disable-setuid-sandbox")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--shm-size=8gb")
	chrome_options.add_argument("--disk-cache-size=0")
	chrome_options.add_argument("--media-cache-size=0")
	chrome_options.add_argument("--ignore-certificate-errors")
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--disable-impl-side-painting")
	chrome_options.add_argument("--disable-seccomp-filter-sandbox")
	chrome_options.add_argument("--disable-breakpad")
	chrome_options.add_argument("--disable-cast")
	chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
	chrome_options.add_argument("--disable-cloud-import")
	
	headless = True
	chromedriver = '/usr/bin/chromedriver'
	if 'env' in config:
		if 'chromedriver' in config['env']:
			chromedriver = config['env']['chromedriver']

		if 'headless' in config['env']:
			headless =  config['env']['headless']

	if headless:
		chrome_options.add_argument("--headless")

	# print(chrome_options.arguments)

	driver = webdriver.Chrome(chromedriver, options=chrome_options)
	return driver

def navigate(driver, url):
	"""
	navigate a driver instance to a url
	"""
	try:
		driver.get(url)
		time.sleep(constantsModule.PAGE_LOAD_WAIT_TIME_DEFAULT)
	except:
		err = sys.exc_info()[0]
		LOGGER.warning(f"url not reachable: {url}")
		LOGGER.error(err)

	return driver

def close(driver):
	"""
	closes a broser driver instance
	"""
	try:
		if driver:
			driver.close()
			return True
		return False
	except:
		err = sys.exc_info()[0]
		LOGGER.warning("cannot close browser instance.")
		LOGGER.error(err)
		return False
