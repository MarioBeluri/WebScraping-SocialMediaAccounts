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
website = "https://swapsocials.com/instagram-accounts-for-sale/"

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
number_of_pages = 20

while (i < number_of_pages - 1):
    elements = driver.find_elements("xpath", "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/ul/li/div[@class = 'nm-shop-loop-thumbnail nm-loader']/a")

    for element in elements:
        link = element.get_attribute("href")

        original_window = driver.current_window_handle

        driver.switch_to.new_window('tab')
        driver.get(link)
        driver.switch_to.window(driver.window_handles[1])

        sleep(5)

        names_element = driver.find_element("xpath", "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[1]/h1")

        category_element = driver.find_element("xpath",
                                               "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div/div[1]/nav/a[3]")
        subscribed_element = driver.find_element("xpath",
                                                 "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/p[2]/strong[1]")
        price_element = driver.find_element("xpath",
                                            "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[1]/p/span/bdi")
        description_element = driver.find_element("xpath", "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/p[3]")

        average_likes_element = driver.find_element("xpath",
                                                 "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/p[2]")

        names.append(names_element.text)
        category.append(category_element.text)
        subscribed.append(subscribed_element.getText())
        prices.append(price_element.text)
        descriptions.append(description_element.text)
        average_likes.append(average_likes_element.getText())
        social_media.append("Instagram")

        driver.close()
        driver.switch_to.window(original_window)
        sleep(2)
    next_page = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/nav/ul/li[11]/a")
    next_page_click = next_page.get_attribute("href")
    next_page_click.click()
    i += 1

print(names, category, subscribed, prices, descriptions, average_likes, social_media)