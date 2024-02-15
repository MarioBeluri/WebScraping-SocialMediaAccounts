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
URLs = []
sellers = []
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
views = []
emails = []
promotions = []
supports = []
contents = []
source_expense = []
source_income = []

driver.get(website)
sleep(30)

while True:
    elements = driver.find_elements("xpath", "/html/body/main/div[1]/div/div[4]/div/div/div[@class = 'post__more']/a")

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

        group_data_div = driver.find_element(By.CLASS_NAME,"group-data")
        paragraphs = group_data_div.find_elements(By.TAG_NAME, "p")
        emails.append(paragraphs[0].text.split(":")[1].strip())
        promotions.append(paragraphs[1].text.split(":")[1].strip())
        source_expense.append(paragraphs[2].text.split(":")[1].strip())
        source_income.append(paragraphs[3].text.split(":")[1].strip())
        supports.append(paragraphs[4].text.split(":")[1].strip())
        contents.append(paragraphs[5].text.split(":")[1].strip())
        seller_name_div = driver.find_element(By.CLASS_NAME,"right-top__name")
        seller_element = seller_name_div.find_element(By.CLASS_NAME,"bold")
        names_element = driver.find_element("xpath", "/html/body/main/div/div/div[@class = 'group-info group']/div[@class = 'group-info']/h1/span")

        categoryAndAddress_element = driver.find_element("xpath",
                                               "/html/body/main/div/div/div[3]/div[2]/p")
        subscribed_element = driver.find_element("xpath",
                                                 "/html/body/main/div/div/div[3]/div[2]/div[1]/p[1]")
        price_element = driver.find_element("xpath",
                                            "/html/body/main/div/div/div[3]/div[2]/div[2]")
        listed_date_element = driver.find_element("xpath",
                                                  "/html/body/main/div/div/div[2]/span[1]")
        views_element = driver.find_element("xpath", "/html/body/main/div/div/div[2]/span[3]")
        description_element = driver.find_element("xpath", "/html/body/main/div/div/div[4]/div/div[1]/p[2]")
        address_element = driver.find_element("xpath", "/html/body/main/div/div/div[3]/div[2]/p/a")
        monthly_income_element = driver.find_element("xpath",
                                                 "/html/body/main/div/div/div[3]/div[2]/div[1]/p[2]")
        monthly_expense_element = driver.find_element("xpath",
                                                 "/html/body/main/div/div/div[3]/div[2]/div[1]/p[3]")

        splitCandA = categoryAndAddress_element.text.split('|')
        names.append(names_element.text)
        categories.append(splitCandA[0].strip())
        followers.append(subscribed_element.text)
        prices.append(price_element.text)
        listed_dates.append(listed_date_element.text)
        descriptions.append(description_element.text)
        monthly_expenses.append(monthly_expense_element.text)
        monthly_incomes.append(monthly_income_element.text)
        address.append(splitCandA[0].strip())
        social_media.append("Twitter")
        sellers.append(seller_element.text)
        views.append(views_element.text)

        driver.close()
        driver.switch_to.window(original_window)
        sleep(2)
    try:
        next_page = driver.find_element(By.XPATH, "//div[@class='pagination']/a[@class='next']")
        next_page.click()
    except:
        break

print(names, categories, followers, prices, listed_dates, descriptions, monthly_expenses, monthly_incomes, address, social_media)