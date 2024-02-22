import time
from hashlib import new
from telnetlib import EC

from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.common.by import By

social_media_urls = {
    "Twitter": "https://www.z2u.com/twitter/accounts-5-15142",
    "Instagram": "https://www.z2u.com/instagram/accounts-5-15129",
    "Facebook": "https://www.z2u.com/facebook/accounts-5-15128"
}

def scrape_data(driver, url, social_media, collection):
    login = "https://www.z2u.com/"

    i = 0
    j = 2

    driver.get(login)
    time.sleep(120)
    driver.get(url)
    time.sleep(3)

    paging_element = driver.find_element(By.CLASS_NAME, "M-box11")

    # Find all the page number links
    page_number_links = paging_element.find_elements(By.TAG_NAME, "a")

    # Extract the last page number from the last link
    number_of_pages = int(page_number_links[-3].text)

    while i < number_of_pages - 1:

        elements = driver.find_elements("xpath", "//div[@class = 'row wrapper shop_list']/div//a")

        for element in elements:
            link = element.get_attribute("href")
            original_window = driver.current_window_handle
            URL = link

            driver.switch_to.new_window('tab')
            driver.get(link)
            time.sleep(10)

            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    break

            try:
                title = driver.find_element(By.XPATH, "//div[@class = 'combin-light-bg-wrap']/h2").text
            except Exception as e:
                print("Error finding title:", e)
                title = None

            try:
                seller = driver.find_element(By.CLASS_NAME, 'seller__name').text
            except Exception as e:
                print("Error finding seller:", e)
                seller = None

            try:
                info_element = driver.find_element(By.CSS_SELECTOR, ".boxbottom.dengji.flex_between .u-info li")
                text = info_element.text
                parts = text.split("\n")
                total_order = parts[0].split(": ")[1]
                positive_rating = parts[1].split(': ')[1].split(' ')[0]
                positive_review = parts[1].split('(')[1].split(')')[0]
            except Exception as e:
                print("Error finding seller info:", e)
                total_order = None
                positive_rating = None
                positive_review = None

            try:
                offer_id = driver.find_element(By.CLASS_NAME, "wenbenright").text.split('#')[1]
            except Exception as e:
                print("Error finding offer id:", e)
                offer_id = None

            try:
                offer = driver.find_element(By.CSS_SELECTOR, ".more-offers strong").text
            except Exception as e:
                print("Error finding offers:", e)
                offer = None

            try:
                price = driver.find_element(By.CLASS_NAME, "price").text
            except Exception as e:
                print("Error finding price:", e)
                price = None

            try:
                description = driver.find_element(By.CLASS_NAME, "wb_text_in").text
            except Exception as e:
                print("Error finding description:", e)
                description = None

            social_medias = social_media

            try:
                entry_data = {
                    "url": URL,
                    "title": title,
                    "seller": seller,
                    "total_order": total_order,
                    "rating_pct": positive_rating,
                    "rating_count": positive_review,
                    "offer_id": offer_id,
                    "pending_offers": offer,
                    "description": description,
                    "price": price,
                    "social_media": social_medias
                }
                collection.insert_one(entry_data)
            except Exception as e:
                print("Error Occurred:", e)
                client.close()
                print("Connection Closed")

            driver.close()
            driver.switch_to.window(original_window)
            time.sleep(2)

        clickable = driver.find_element(By.LINK_TEXT, str(j))
        clickable.click()
        i += 1
        j += 1

    driver.close()

# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, Facebook): ")

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
    print("Web Scraping finished")
else:
    print("Invalid social media platform. Please enter a valid Social Media platform.")