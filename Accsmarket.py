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
website = "https://accsmarket.com/en/catalog/twitter" #Twitter

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

listings = driver.find_elements(By.XPATH, "//div[@class = 'soc-text']/p/a")
prices = [price.get_attribute("textContent") for price in driver.find_elements(By.XPATH, "//div[@class = 'soc-price']/div")]
descriptions = [listing.get_attribute("text") for listing in listings]
social_media = ["Twitter" for _ in range(len(listings))]

for i in range(len(prices)):
    index_of_dollar = prices[i].find('$')
    if index_of_dollar != -1:
        prices[i] = prices[i][index_of_dollar:].strip()
driver.close()

print(prices, descriptions, social_media)