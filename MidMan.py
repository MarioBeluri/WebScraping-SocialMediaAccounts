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

social_media_urls = {
    "Twitter": "https://mid-man.com/twitter/",
    "Instagram": "https://mid-man.com/instagram/",
    "Youtube": "https://mid-man.com/youtube/",
    "Facebook": "https://mid-man.com/facebook/",
    "Tiktok": "https://mid-man.com/tiktok/"
}

def scrape_data(driver, url, social_media, collection):
    driver.get(url)
    i = 0
    URLs = []
    names = []
    social_medias = []
    followers = []
    prices = []
    categories = []

    while True:

        try:
            names_element = driver.find_elements("xpath", "//div[@class = 'product-shop-area']/div/div/div/div/div/a")
            category_element = driver.find_elements("xpath",
                                                    "//div[@class = 'product-shop-area']/div/div/div/div/div/div[@class='product-topic']")
            subscribed_element = driver.find_elements("xpath",
                                                      "//div[@class = 'product-shop-area']/div/div/div/div/div/ul[@class='list-inline list-meta mb-0']/li[@class='list-inline-item list-follow']")
            for j in range(len(names_element)):
                URLs.append(names_element[j].get_attribute("href"))
                names.append(names_element[j].text)
                categories.append(category_element[j].text)
                followers.append(subscribed_element[j].text)
                social_medias.append(social_media)
                try:
                    price_element = driver.find_elements(By.XPATH, "//p[@class='price']//span[not(ancestor::ins)]/bdi")
                    if not price_element[j].text:
                        prices.append("75")
                    else:
                        prices.append(price_element[j].text)
                except:
                    # Handle the case where the element is not found
                    prices.append("50")
        except Exception as e:
            print("Error occurred while extracting elements information:", e)
            URLs.append(None)
            names.append(None)
            categories.append(None)
            followers.append(None)
            social_medias.append(None)
            prices.append(None)

        try:
            for j in range(len(names_element)):
                entry_data = {
                    "url": URLs[j],
                    "title": names[j],
                    "category": categories[j],
                    "price": prices[j],
                    "social_media": social_medias[j],
                    "followers": followers[j],
                }
                collection.insert_one(entry_data)
            URLs.clear()
            names.clear()
            categories.clear()
            prices.clear()
            social_medias.clear()
            followers.clear()
        except:
            print("Error Occured")

        try:
            next_page_link = driver.find_element(By.XPATH, "//a[@class='next page-numbers']")
            next_page_link.click()
            sleep(5)
        except:
            break

# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, Facebook, Tiktok, Youtube): ")

# Validate user input and scrape data accordingly
if social_media_input in social_media_urls:
    driver = Driver(uc=True)
    client = MongoClient()
    db = client.WebScraping
    collection = db.WebScraping
    scrape_data(driver, social_media_urls[social_media_input], social_media_input, collection)
    driver.quit()
    client.close()
    print("Connection Closed")
    print("Scraping finished")
else:
    print("Invalid social media platform. Please enter a valid Social Media platform.")
