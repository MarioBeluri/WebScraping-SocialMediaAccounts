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

driver = Driver(uc=True)
website = "https://swapsocials.com/instagram-accounts-for-sale/"

i = 0
URLs = []
names = []
social_media = []
address = []
followers = []
prices = []
descriptions = []
listed_dates = []
categories = []
monthly_incomes = []
monthly_expenses = []
average_likes = []

driver.get(website)

ul_element = driver.find_element(By.CSS_SELECTOR,'.page-numbers')

li_elements = ul_element.find_elements(By.TAG_NAME,'li')

number_of_pages = li_elements[-2].text

while i < int(number_of_pages) - 1:
    elements = driver.find_elements("xpath", "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/ul/li/div[@class = 'nm-shop-loop-thumbnail nm-loader']/a")

    for element in elements:
        link = element.get_attribute("href")

        URLs.append(link)
        original_window = driver.current_window_handle

        driver.switch_to.new_window('tab')
        driver.get(link)
        sleep(2)
        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break
        sleep(5)

        try:
            names_element = driver.find_element("xpath",
                                                "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[1]/h1")
            names.append(names_element.text)
        except Exception as e:
            print("Error occurred while extracting names information:", e)
            names.append(None)

        try:
            category_element = driver.find_element("xpath",
                                                   "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div/div[1]/nav/a[3]")
            categories.append(category_element.text)
        except Exception as e:
            print("Error occurred while extracting category information:", e)
            categories.append(None)

        try:
            subscribedAndAverageLikes_element = driver.find_element(By.XPATH,
                                                                    "//div[@class='woocommerce-product-details__short-description']//p[2]")
            subAndLikes = subscribedAndAverageLikes_element.text
            split_index = subAndLikes.index('\n')
            followers_string = subAndLikes[:split_index]
            likes_string = subAndLikes[split_index + 1:]
            followers_split = followers_string.split(":")
            followers.append(followers_split[1].strip())
            likes_split = likes_string.split(":")
            average_likes.append(likes_split[1].strip())
        except Exception as e:
            print("Error occurred while extracting followers information:", e)
            followers.append(None)
            average_likes.append(None)

        try:
            price_element = driver.find_elements("xpath",
                                                 "//p[@class='price']//span[@class='woocommerce-Price-amount amount']/bdi")
            prices.append(price_element[0].text)
        except Exception as e:
            print("Error occurred while extracting price information:", e)
            prices.append(None)

        try:
            description_element = driver.find_element("xpath",
                                                      "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/p[3]")
            descriptions.append(description_element.text)
        except Exception as e:
            print("Error occurred while extracting description information:", e)
            descriptions.append(None)

        social_media.append("Instagram")

        driver.close()
        driver.switch_to.window(original_window)
        sleep(2)

    next_page = driver.find_element(By.XPATH,
                                    "//nav[@class='woocommerce-pagination nm-pagination nm-infload']//a[@class='next page-numbers']")
    next_page_click = next_page.get_attribute("href")
    next_page_click.click()
    i += 1

driver.quit()
print(names, categories, followers, prices, listed_dates, descriptions, monthly_expenses, monthly_incomes, address, social_media)