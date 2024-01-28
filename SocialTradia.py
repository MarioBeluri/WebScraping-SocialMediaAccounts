from hashlib import new
from telnetlib import EC
import re

from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from time import sleep

driver = Driver(uc=True)

website = "https://socialtradia.com/product-categories/"  # Categories
xpath_expressions = [
    "/html/body/div/div[1]/div/div[2]/div/div[2]/div/div/div/ul/li/div[2]/div/div[@class='nm-shop-loop-price']/span/del/span/span",
    "/html/body/div/div[1]/div/div[2]/div/div[2]/div/div/div/ul/li/div[2]/div/div[@class='nm-shop-loop-price']/span/span/span"
]

social_media = []
names = []
subscribed = []
prices = []
listed_dates = []
descriptions = []
category = []
monthly_income = []
monthly_expense = []
address = []

driver.get(website)

number_of_categories = driver.find_elements(By.XPATH, "//div[1]/div/div[1]/div[3]/div/div[@class='nm_column col-sm-4 mt-4']/a")

for categories in number_of_categories:

    categories_link = categories.get_attribute("href")

    original_window = driver.current_window_handle

    driver.switch_to.new_window('tab')
    driver.get(categories_link)
    driver.switch_to.window(driver.window_handles[0])

    number_of_pages_element = driver.wait_for_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/nav/ul/li[8]/a")
    number_of_pages = int(number_of_pages_element.text)
    i = 0
    while i < number_of_pages - 1:

        names_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/ul/li/div/h3/a")
        category_element = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/h1/span")

        price_element = price_element = driver.find_element(By.CLASS_NAME, "woocommerce-Price-amount")

        for name_element in names_elements:
            # Extract the text content from the name element
            name_and_followers = name_element.text.split("(")

            name = name_and_followers[0].strip()
            subscribed_number = name_and_followers[1].split(")")[0].strip()

            names.append(name)
            category.append(category_element.text)
            subscribed.append(subscribed_number)
            prices.append(price_element.text)
            address.append(name)
            social_media.append("Instagram")
        i += 1
        next_page = driver.find_elements(By.XPATH,"/html/body/div/div[1]/div/div[2]/div/div[2]/div/div/div/nav/ul/li")
        next_page_link = next_page[-1].find_element(By.TAG_NAME, "a")
        next_page_link.click()

    driver.close()
    driver.switch_to.window(original_window)
    sleep(2)

driver.close()
print(names, category, subscribed, prices, listed_dates, descriptions, monthly_expense, monthly_income, address, social_media)
