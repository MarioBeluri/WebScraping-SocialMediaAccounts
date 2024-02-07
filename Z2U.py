from hashlib import new
from telnetlib import EC

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
website = "https://www.z2u.com/twitter/accounts-5-15142" #Twitter

i = 0
social_media = []
names = []
subscribed = []
prices = []
listed_dates = []
descriptions = []
category = []
average_likes = []
address = []

driver.get(website)
number_of_pages = 26

while (i < number_of_pages - 1):

    names_element = driver.find_elements("xpath", "///div[@class = 'row wrapper shop_list']/div//div[@class = 'seller']")

    price_element = driver.find_elements("xpath",
                                            "//div[@class = 'row wrapper shop_list']/div//div[@class = 'priceWrap']")

    description_element = driver.find_elements("xpath", "//div[@class = 'row wrapper shop_list']/div//span[@class = 'title']")

    for j in range(len(names_element) - 1):
        names.append(names_element[j].text)
        descriptions.append(description_element[j].text)
        prices.append(price_element[j].text)
        social_media.append("Twitter")


    next_page.click()
    i += 1

driver.close()

print(names, category, subscribed, prices, descriptions, average_likes, social_media)