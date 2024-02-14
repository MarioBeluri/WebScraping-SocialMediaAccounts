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

driver.get(login)
time.sleep(90)
driver.get(website)
time.sleep(3)
number_of_pages = 26

while (i < number_of_pages - 1):

    clickable = driver.find_element(By.CLASS_NAME, "next")
    clickable.click()


    names_element = driver.find_elements("xpath", "///div[@class = 'row wrapper shop_list']/div//div[@class = 'seller']")

    price_element = driver.find_elements("xpath",
                                            "//div[@class = 'row wrapper shop_list']/div//div[@class = 'priceWrap']")

    description_element = driver.find_elements("xpath", "//div[@class = 'row wrapper shop_list']/div//span[@class = 'title']")

    for j in range(len(names_element) - 1):
        names.append(names_element[j].text)
        descriptions.append(description_element[j].text)
        prices.append(price_element[j].text)
        social_media.append("Twitter")


    #next_page.click()
    i += 1

driver.close()

print(names, categories, followers, prices, listed_dates, descriptions, monthly_expenses, monthly_incomes, address, social_media)