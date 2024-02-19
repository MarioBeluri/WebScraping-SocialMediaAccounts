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
from db_util import MongoDBActor
from selenium_driver_util import PageDriver


# Define a dictionary to map social media platforms to URLs
social_media_urls = {
    "Twitter": "https://accs-market.com/twitter",
    "Instagram": "https://accs-market.com/in",
    "YouTube": "https://accs-market.com/youtube",
    "Facebook": "https://accs-market.com/fb",
    "TikTok": "https://accs-market.com/tiktok"
}

# Function to scrape data for a given social media platform URL
def scrape_data(driver, url, socialMedia):
    driver.get(url)
    sleep(30)  # Adjust the sleep time as needed

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
    views = []
    emails = []
    promotions = []
    supports = []
    contents = []
    source_expense = []
    source_income = []

    while True:
        elements = driver.find_elements(By.XPATH, "//div[@class='post__more']/a")

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

            group_data_div = driver.find_element(By.CLASS_NAME, "group-data")
            paragraphs = group_data_div.find_elements(By.TAG_NAME, "p")
            emails.append(paragraphs[0].text.split(":")[1].strip())
            promotions.append(paragraphs[1].text.split(":")[1].strip())
            source_expense.append(paragraphs[2].text.split(":")[1].strip())
            source_income.append(paragraphs[3].text.split(":")[1].strip())
            supports.append(paragraphs[4].text.split(":")[1].strip())
            contents.append(paragraphs[5].text.split(":")[1].strip())
            seller_name_div = driver.find_element(By.CLASS_NAME, "right-top__name")
            seller_element = seller_name_div.find_element(By.CLASS_NAME, "bold")
            names_element = driver.find_element("xpath",
                                                "/html/body/main/div/div/div[@class = 'group-info group']/div[@class = 'group-info']/h1/span")

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
            address.append(splitCandA[1].strip())
            social_media.append(socialMedia)
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

    print(names, categories, followers, prices, listed_dates, descriptions, monthly_expenses, monthly_incomes, address,
          social_media)


# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, YouTube, Facebook, TikTok): ")

# Validate user input and scrape data accordingly
if social_media_input in social_media_urls:
    driver = Driver(uc=True)
    scrape_data(driver, social_media_urls[social_media_input], social_media_input)
    driver.quit()
else:
    print("Invalid social media platform. Please enter a valid Social Media platform.")
