import time
from hashlib import new
from telnetlib import EC

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.common.by import By

#options = Options()
#options.add_experimental_option("detach", True)
#driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = Driver(uc=True)
login = "https://www.z2u.com/"
website = "https://www.z2u.com/twitter/accounts-5-15142" #Twitter

i = 0
j=2
sellers = []
URLs = []
titles = []
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
positive_reviews = []
positive_rating = []
total_orders = []
offer_ids = []
offers = []

#driver.get(login)
#time.sleep(90)
driver.get(website)
time.sleep(3)
number_of_pages = 26

while (i < number_of_pages - 1):

    elements = driver.find_elements("xpath", "//div[@class = 'row wrapper shop_list']/div//a")

    for element in elements:
        link = element.get_attribute("href")
        original_window = driver.current_window_handle
        URLs.append(link)

        driver.switch_to.new_window('tab')
        driver.get(link)
        time.sleep(2)

        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break

        titles.append(driver.find_element(By.XPATH, "//div[@class = 'combin-light-bg-wrap']/h2").text)
        sellers.append(driver.find_element(By.CLASS_NAME, 'seller__name').text)

        info_element = driver.find_element(By.CSS_SELECTOR,".boxbottom.dengji.flex_between .u-info li")
        text = info_element.text
        parts = text.split("\n")
        total_orders.append(parts[0].split(": ")[1])
        positive_rating.append(parts[1].split(': ')[1].split(' ')[0])
        positive_reviews.append(parts[1].split('(')[1].split(')')[0])

        offer_ids.append(driver.find_element(By.CLASS_NAME, "wenbenright").text.split('#')[1])
        offers.append( driver.find_element(By.CSS_SELECTOR,".more-offers strong").text)
        prices.append(driver.find_element(By.CLASS_NAME,"price").text)
        descriptions.append(driver.find_element(By.CLASS_NAME, "wb_text_in").text)
        social_media.append("Twitter")
        driver.close()
        driver.switch_to.window(original_window)
        time.sleep(2)

    clickable = driver.find_element(By.LINK_TEXT, j)
    clickable.click()
    i += 1
    j += 1

driver.close()

print(names, categories, followers, prices, listed_dates, descriptions, monthly_expenses, monthly_incomes, address, social_media)