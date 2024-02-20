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
    email_included = []
    promotions = []
    supports = []
    contents = []
    source_expense = []
    source_income = []
    monetization_enabled = []

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

            try:
                group_data_div = driver.find_element(By.CLASS_NAME, "group-data")
                paragraphs = group_data_div.find_elements(By.TAG_NAME, "p")
                for paragraph in paragraphs:
                    text = paragraph.text
                    if 'Original' in text:
                        email_included.append(text.split(":")[-1].strip())
                    elif 'Ways' in text:
                        promotions.append(text.split(":")[-1].strip())
                    elif 'expense' in text:
                        source_expense.append(text.split(":")[-1].strip())
                    elif 'income' in text:
                        source_income.append(text.split(":")[-1].strip())
                    elif 'support' in text:
                        supports.append(text.split(":")[-1].strip())
                    elif 'Content' in text:
                        contents.append(text.split(":")[-1].strip())
                    elif 'Monetization ' in text:
                        monetization_enabled.append(text.split(":")[-1].strip())
            except Exception as e:
                print("Error occurred while extracting group data:", e)

            try:
                seller_name_div = driver.find_element(By.CLASS_NAME, "right-top__name")
                seller_element = seller_name_div.find_element(By.CLASS_NAME, "bold")
                sellers.append(seller_element.text)
            except Exception as e:
                print("Error occurred while extracting seller data:", e)
                sellers.append(None)

            try:
                names_element = driver.find_element("xpath",
                                                    "/html/body/main/div/div/div[@class = 'group-info group']/div[@class = 'group-info']/h1/span")
                names.append(names_element.text)
            except Exception as e:
                print("Error occurred while extracting names data:", e)
                names.append(None)

            try:
                categoryAndAddress_element = driver.find_element("xpath",
                                                                 "/html/body/main/div/div/div[3]/div[2]/p")
                splitCandA = categoryAndAddress_element.text.split('|')
                categories.append(splitCandA[0].strip())
                address.append(splitCandA[1].strip())
            except Exception as e:
                print("Error occurred while extracting category and address data:", e)
                categories.append(None)
                address.append(None)

            try:
                subscribed_element = driver.find_element("xpath",
                                                         "/html/body/main/div/div/div[3]/div[2]/div[1]/p[1]")
                subSplit = subscribed_element.text.split('-')
                followers.append(subSplit[0].strip())
            except Exception as e:
                print("Error occurred while extracting subscribed data:", e)
                followers.append(None)

            try:
                price_element = driver.find_element("xpath",
                                                    "/html/body/main/div/div/div[3]/div[2]/div[2]")
                prices.append(price_element.text)

            except Exception as e:
                print("Error occurred while extracting price data:", e)
                prices.append(None)

            try:
                listed_date_element = driver.find_element("xpath",
                                                          "/html/body/main/div/div/div[2]/span[1]")
                listedSplit = listed_date_element.text.split(":")
                listed_dates.append(listedSplit[1].strip())
            except Exception as e:
                print("Error occurred while extracting listed date data:", e)
                listed_dates.append(None)

            try:
                views_element = driver.find_element("xpath", "/html/body/main/div/div/div[2]/span[3]")
                viewsSplit = views_element.text.split(":")
                views.append(viewsSplit[1].strip())
            except Exception as e:
                print("Error occurred while extracting views data:", e)
                views.append(None)

            try:
                description_element = driver.find_element("xpath",
                                                          "/html/body/main/div/div/div[4]/div/div[1]/p[2]")
                descriptions.append(description_element.text)
            except Exception as e:
                print("Error occurred while extracting description data:", e)
                descriptions.append(None)

            try:
                monthly_income_element = driver.find_element("xpath",
                                                             "/html/body/main/div/div/div[3]/div[2]/div[1]/p[2]")
                monthly_expense_element = driver.find_element("xpath",
                                                              "/html/body/main/div/div/div[3]/div[2]/div[1]/p[3]")
                expensesSplit = monthly_expense_element.text.split("-")
                monthly_expenses.append(expensesSplit[0].strip())
                incomeSplit = monthly_income_element.text.split("-")
                monthly_incomes.append(incomeSplit[0].strip())
            except Exception as e:
                print("Error occurred while extracting monthly income and expense data:", e)
                monthly_expenses.append(None)
                monthly_incomes.append(None)

            social_media.append(socialMedia)

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
