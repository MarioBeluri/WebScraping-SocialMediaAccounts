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
        subscribedAndAverageLikes_element = driver.find_element(By.XPATH,
                                                 "//div[@class='woocommerce-product-details__short-description']//p[2]")
        price_element = driver.find_elements("xpath",
                                            "//p[@class='price']//span[@class='woocommerce-Price-amount amount']/bdi")
        description_element = driver.find_element("xpath", "/html/body/div[1]/div[1]/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/p[3]")

        names.append(names_element.text)
        category.append(category_element.text)

        subAndLikes = subscribedAndAverageLikes_element.text
        split_index = subAndLikes.index('\n')
        followers_string = subAndLikes[:split_index]
        likes_string = subAndLikes[split_index + 1:]
        followers_split = followers_string.split(":")
        subscribed.append(followers_split[1].strip())
        prices.append(price_element[0].text)
        likes_split = followers_string.split(":")
        average_likes.append(likes_split[1].strip())

        descriptions.append(description_element.text)
        social_media.append("Instagram")

        driver.close()
        driver.switch_to.window(original_window)
        sleep(2)

    next_page = driver.find_element(By.XPATH,
                                    "//nav[@class='woocommerce-pagination nm-pagination nm-infload']//a[@class='next page-numbers']")
    next_page_click = next_page.get_attribute("href")
    next_page_click.click()
    i += 1

print(names, category, subscribed, prices, descriptions, average_likes, social_media)