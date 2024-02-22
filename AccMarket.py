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
    "Youtube": "https://accs-market.com/youtube",
    "Facebook": "https://accs-market.com/fb",
    "Tiktok": "https://accs-market.com/tiktok"
}

# Function to scrape data for a given social media platform URL
def scrape_data(driver, url, socialMedia, collection):
    driver.get(url)
    sleep(30)  # Adjust the sleep time as needed

    while True:
        elements = driver.find_elements(By.XPATH, "//div[@class='post__more']/a")

        for element in elements:
            link = element.get_attribute("href")
            URL = link
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
                        email_included = text.split(":")[-1].strip()
                    elif 'Ways' in text:
                        promotion = text.split(":")[-1].strip()
                    elif 'expense' in text:
                        source_expense = text.split(":")[-1].strip()
                    elif 'income' in text:
                        source_income = text.split(":")[-1].strip()
                    elif 'support' in text:
                        supports = text.split(":")[-1].strip()
                    elif 'Content' in text:
                        content = text.split(":")[-1].strip()
                    elif 'Monetization ' in text:
                        monetization_enabled = text.split(":")[-1].strip()
            except Exception as e:
                print("Error occurred while extracting group data:", e)

            try:
                seller_name_div = driver.find_element(By.CLASS_NAME, "right-top__name")
                seller_element = seller_name_div.find_element(By.CLASS_NAME, "bold")
                seller = seller_element.text
            except Exception as e:
                print("Error occurred while extracting seller data:", e)
                seller = None

            try:
                names_element = driver.find_element("xpath",
                                                    "/html/body/main/div/div/div[@class = 'group-info group']/div[@class = 'group-info']/h1/span")
                name = names_element.text
            except Exception as e:
                print("Error occurred while extracting names data:", e)
                name = None

            try:
                categoryAndAddress_element = driver.find_element("xpath",
                                                                 "/html/body/main/div/div/div[3]/div[2]/p")
                splitCandA = categoryAndAddress_element.text.split('|')
                categorie = splitCandA[0].strip()
                address = splitCandA[1].strip()
            except Exception as e:
                print("Error occurred while extracting category and address data:", e)
                categorie = None
                address = None

            try:
                subscribed_element = driver.find_element("xpath",
                                                         "/html/body/main/div/div/div[3]/div[2]/div[1]/p[1]")
                subSplit = subscribed_element.text.split('-')
                follower = subSplit[0].strip()
            except Exception as e:
                print("Error occurred while extracting subscribed data:", e)
                follower = None

            try:
                price_element = driver.find_element("xpath",
                                                    "/html/body/main/div/div/div[3]/div[2]/div[2]")
                price = price_element.text

            except Exception as e:
                print("Error occurred while extracting price data:", e)
                price = None

            try:
                listed_date_element = driver.find_element("xpath",
                                                          "/html/body/main/div/div/div[2]/span[1]")
                listedSplit = listed_date_element.text.split(":")
                listed_date = listedSplit[1].strip()
            except Exception as e:
                print("Error occurred while extracting listed date data:", e)
                listed_date = None

            try:
                views_element = driver.find_element("xpath", "/html/body/main/div/div/div[2]/span[3]")
                viewsSplit = views_element.text.split(":")
                view = viewsSplit[1].strip()
            except Exception as e:
                print("Error occurred while extracting views data:", e)
                view = None

            try:
                description_element = driver.find_element("xpath",
                                                          "/html/body/main/div/div/div[4]/div/div[1]/p[2]")
                description = description_element.text
            except Exception as e:
                print("Error occurred while extracting description data:", e)
                description = None

            try:
                monthly_income_element = driver.find_element("xpath",
                                                             "/html/body/main/div/div/div[3]/div[2]/div[1]/p[2]")
                monthly_expense_element = driver.find_element("xpath",
                                                              "/html/body/main/div/div/div[3]/div[2]/div[1]/p[3]")
                expensesSplit = monthly_expense_element.text.split("-")
                monthly_expense = expensesSplit[0].strip()
                incomeSplit = monthly_income_element.text.split("-")
                monthly_income = incomeSplit[0].strip()
            except Exception as e:
                print("Error occurred while extracting monthly income and expense data:", e)
                monthly_expense = None
                monthly_income = None

            social_media = socialMedia

            try:
                if social_media == "Twitter" or social_media == "Instagram" or social_media == "Facebook":
                    entry_data = {
                        "url": URL,
                        "title": name,
                        "seller": seller,
                        "listed_date": listed_date,
                        "price": price,
                        "social_media": social_media,
                        "views": view,
                        "description": description,
                        "followers": follower,
                        "category": categorie,
                        "social_media_address": address,
                        "monthly_income": monthly_income,
                        "monthly_expense": monthly_expense,
                        "email_included": email_included,
                        "promotions": promotion,
                        "source_expense": source_expense,
                        "source_income": source_income,
                        "support_account": supports,
                        "content": content
                    }
                else:
                    entry_data = {
                        "url": URL,
                        "title": name,
                        "seller": seller,
                        "listed_date": listed_date,
                        "price": price,
                        "social_media": social_media,
                        "views": view,
                        "description": description,
                        "followers": follower,
                        "category": categorie,
                        "social_media_address": address,
                        "monthly_income": monthly_income,
                        "monthly_expense": monthly_expense,
                        "monetization_enabled": monetization_enabled,
                        "promotions": promotion,
                        "source_expense": source_expense,
                        "source_income": source_income,
                        "support_account": supports,
                        "content": content
                    }
                collection.insert_one(entry_data)

            except Exception as e:
                print("Error Occurred:", e)
                client.close()
                print("Connection Closed")

            driver.close()
            driver.switch_to.window(original_window)
            sleep(2)
        try:
            next_page = driver.find_element(By.XPATH, "//div[@class='pagination']/a[@class='next']")
            next_page.click()
        except:
            break

# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, Youtube, Facebook, Tiktok): ")

# Validate user input and scrape data accordingly
if social_media_input in social_media_urls:
    driver = Driver(uc=True)
    client = MongoClient()
    db = client.WebScraping
    collection = db.WebScraping
    scrape_data(driver, social_media_urls[social_media_input], social_media_input, collection)
    client.close()
    print("Connection Closed")
    driver.quit()
    print("Scraping finished")
else:
    print("Invalid social media platform. Please enter a valid Social Media platform.")
