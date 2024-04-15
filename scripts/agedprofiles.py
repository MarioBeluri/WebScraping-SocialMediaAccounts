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
	Data scraper for https://agedprofiles.com/

	Catalogs
	-------------
	Youtube/Instagram: https://agedprofiles.com/

	Usage
	-------------
	$ venv/bin/python3 -m scripts.agedprofiles --conf=$(pwd)/local.config.yaml

	
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

def main():
	CONFIG_FILE_DEFAULT = os.path.join(constantsModule.BASE_DIR, 'config.yaml')
	p = argparse.ArgumentParser(description='This script runs the scraper.')
	p.add_argument('--conf', "-C",
					metavar="FILE",
					default=CONFIG_FILE_DEFAULT,
					help='configuration file. (default: %(default)s)',
					type=str)

	global DEBUG
	args= vars(p.parse_args())
	config = IOModule.load_config_yaml(args["conf"])

	if "env" in config:
		if "output_dir" in config["env"]:
			constantsModule.OUTPUT_DIR = config["env"]["output_dir"]

		if "debug" in config["env"]:
			d = str(config["env"]["debug"]).lower()
			if d == "true":
				DEBUG = True


	filename = "agedprofiles_" + utilityModule.get_timestamp() + '.json'
	output_file = os.path.join(constantsModule.OUTPUT_DIR, filename)

	LOGGER.info("spawn selenium instance.")
	driver = driverModule.get_new_browser_instance(config)

	website_url =  "https://agedprofiles.com/"
	LOGGER.info(f'[agedprofiles] started scraping')
	driver = driverModule.navigate(driver, website_url)
	
	## TODO:
	script="""

	"""

	data = driver.execute_script(script)

	driverModule.close(driver)
	LOGGER.info(f'[agedprofiles] finished scraping')

	utilityModule.save_json_output(output_file, data)
	LOGGER.info("saved all records with length: %s"%str(len(data)))

if __name__ == "__main__":
	main()


