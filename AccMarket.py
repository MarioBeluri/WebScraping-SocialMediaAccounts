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

while (i < number_of_pages - 1):
    elements = driver.find_elements("xpath", "/html/body/main/div[1]/div/div[4]/div/div/div[@class = 'post__more']/a")

    for element in elements:
        link = element.get_attribute("href")

        original_window = driver.current_window_handle

        driver.switch_to.new_window('tab')
        driver.get(link)
        driver.switch_to.window(driver.window_handles[0])

        sleep(5)

        names_element = driver.find_element("xpath", "/html/body/main/div/div/div[@class = 'group-info group']/div[@class = 'group-info']/h1/span")

        categoryAndAddress_element = driver.find_element("xpath",
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

        splitCandA = categoryAndAddress_element.text.split('|')
        names.append(names_element.text)
        category.append(splitCandA[0].strip())
        subscribed.append(subscribed_element.text)
        prices.append(price_element.text)
        listed_dates.append(listed_date_element.text)
        descriptions.append(description_element.text)
        monthly_expense.append(monthly_expense_element.text)
        monthly_income.append(monthly_income_element.text)
        address.append(splitCandA[0].strip())
        social_media.append("Twitter")

        driver.close()
        driver.switch_to.window(original_window)
        sleep(2)
    next_page = driver.find_element(By.XPATH, "//div[@class='pagination']/a[@class='next']")
    next_page.click()
    i += 1

print(names, category, subscribed, prices, listed_dates, descriptions, monthly_expense, monthly_income, address, social_media)