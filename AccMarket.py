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
website = "https://accs-market.com/twitter" #Twitter

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
sleep(30)
number_of_pages = 12

while (i < number_of_pages):

    elements = driver.find_elements("xpath", "/html/body/main/div[1]/div/div[4]/div/div/div[@class = 'post__more']/a")

    for element in elements:
        link = element.get_attribute("href")

        driver.execute_script("window.open('', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])

        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/div[@class = 'group-info group']/div[@class = 'group-info']/h1/span")))
        sleep(5)

        names_element = driver.find_element("xpath", "/html/body/main/div/div/div[@class = 'group-info group']/div[@class = 'group-info']/h1/span")
        social_media_element = driver.find_element("xpath", "/html/body/div[1]/div/div[1]/h1/span")
        category_element = driver.find_element("xpath",
                                               "/html/body/main/div/div/div[3]/div[2]/p")
        subscribed_element = driver.find_element("xpath",
                                                 "/html/body/main/div/div/div[3]/div[2]/div[1]/p[1]")
        price_element = driver.find_element("xpath",
                                            "/html/body/main/div/div/div[3]/div[2]/div[2]")
        listed_date_element = driver.find_element("xpath",
                                                  "/html/body/main/div/div/div[2]/span[1]")
        description_element = driver.find_element("xpath", "/html/body/main/div/div/div[4]/div/div[1]/p[2]")
        address_element = driver.find_element("xpath", "/html/body/main/div/div/div[3]/div[2]/p/a")
        monthly_income_element = driver.find_element("xpath",
                                                 "/html/body/main/div/div/div[3]/div[2]/div[1]/p[2]")
        monthly_expense_element = driver.find_element("xpath",
                                                 "/html/body/main/div/div/div[3]/div[2]/div[1]/p[3]")

        names.append(names_element.text)
        category.append(category_element.text)
        subscribed.append(subscribed_element.text)
        prices.append(price_element.text)
        listed_dates.append(listed_date_element.text)
        descriptions.append(description_element.text)
        monthly_expense.append(description_element.text)
        monthly_income.append(description_element.text)
        address.append(description_element.get_attribute("href"))
        social_media.append("Twitter")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(2)
driver.find_element("xpath", "//ul[@class='pagination']/li/a[@rel='next']").click()

print(names, category, subscribed, prices, listed_dates, descriptions, monthly_expense, monthly_income, address, social_media)