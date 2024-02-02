from hashlib import new
from telnetlib import EC

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from time import sleep

#options = Options()
#options.add_experimental_option("detach", True)
#driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = Driver(uc=True)
website = "https://mid-man.com/instagram/" #Instagram

i = 0
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
number_of_pages = 11

while (i < number_of_pages - 1):

    names_element = driver.find_elements("xpath", "//div[@class = 'product-shop-area']/div/div/div/div/div/a")

    category_element = driver.find_elements("xpath",
                                               "//div[@class = 'product-shop-area']/div/div/div/div/div/div[@class='product-topic']")
    subscribed_element = driver.find_elements("xpath",
                                                 "//div[@class = 'product-shop-area']/div/div/div/div/div/ul[@class='list-inline list-meta mb-0']/li[@class='list-inline-item list-follow']")


    for j in range(len(names_element) - 1):
        names.append(names_element[j].text)
        category.append(category_element[j].text)
        subscribed.append(subscribed_element[j].text)
        address.append(names_element[j].text)
        social_media.append("Twitter")

        try:
            price_element = driver.find_elements(By.XPATH,
                                                "//div[@class='product-shop-area']/div/div/div/div/div/ul[2]/li/p/span[@class='woocommerce-Price-amount amount']/bdi")
            # Extract the text content of the element
            prices.append(price_element[j].text)
        except NoSuchElementException:
            # Handle the case where the element is not found
            prices.append("50")

    next_page_link = driver.find_element(By.XPATH, "//a[@class='next page-numbers']")
    next_page_url = next_page_link.get_attribute("href")
    next_page_url.click()
    i += 1


print(names, category, subscribed, prices, listed_dates, descriptions, monthly_expense, monthly_income, address, social_media)