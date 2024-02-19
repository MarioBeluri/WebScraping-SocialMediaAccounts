import time
from hashlib import new
from telnetlib import EC

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.common.by import By

social_media_urls = {
    "Twitter": "https://www.z2u.com/twitter/accounts-5-15142",
    "Instagram": "https://www.z2u.com/instagram/accounts-5-15129",
    "Facebook": "https://www.z2u.com/facebook/accounts-5-15128"
}

def scrape_data(driver, url, social_media):
    login = "https://www.z2u.com/"

    i = 0
    j = 2
    sellers = []
    URLs = []
    titles = []
    names = []
    social_medias = []
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
            URLs.append(link)

            driver.switch_to.new_window('tab')
            driver.get(link)
            time.sleep(10)

            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    break

            try:
                titles.append(driver.find_element(By.XPATH, "//div[@class = 'combin-light-bg-wrap']/h2").text)
            except Exception as e:
                print("Error finding title:", e)
                titles.append(None)

            try:
                sellers.append(driver.find_element(By.CLASS_NAME, 'seller__name').text)
            except Exception as e:
                print("Error finding seller:", e)
                sellers.append(None)

            try:
                info_element = driver.find_element(By.CSS_SELECTOR, ".boxbottom.dengji.flex_between .u-info li")
                text = info_element.text
                parts = text.split("\n")
                total_orders.append(parts[0].split(": ")[1])
                positive_rating.append(parts[1].split(': ')[1].split(' ')[0])
                positive_reviews.append(parts[1].split('(')[1].split(')')[0])
            except Exception as e:
                print("Error finding seller info:", e)
                total_orders.append(None)
                positive_rating.append(None)
                positive_reviews.append(None)

            try:
                offer_ids.append(driver.find_element(By.CLASS_NAME, "wenbenright").text.split('#')[1])
            except Exception as e:
                print("Error finding offer id:", e)
                offer_ids.append(None)

            try:
                offers.append(driver.find_element(By.CSS_SELECTOR, ".more-offers strong").text)
            except Exception as e:
                print("Error finding offers:", e)
                offers.append(None)

            try:
                prices.append(driver.find_element(By.CLASS_NAME, "price").text)
            except Exception as e:
                print("Error finding price:", e)
                prices.append(None)

            try:
                descriptions.append(driver.find_element(By.CLASS_NAME, "wb_text_in").text)
            except Exception as e:
                print("Error finding description:", e)
                descriptions.append(None)

            social_medias.append(social_media)
            driver.close()
            driver.switch_to.window(original_window)
            time.sleep(2)

        clickable = driver.find_element(By.LINK_TEXT, str(j))
        clickable.click()
        i += 1
        j += 1

    driver.close()

    print(names, categories, followers, prices, listed_dates, descriptions, monthly_expenses, monthly_incomes, address, social_media)

# User input for social media platform
social_media_input = input("Enter social media platform (Twitter, Instagram, Facebook): ")

# Validate user input and scrape data accordingly
if social_media_input in social_media_urls:
    driver = Driver(uc=True)
    scrape_data(driver, social_media_urls[social_media_input], social_media_input)
    driver.quit()
else:
    print("Invalid social media platform. Please enter a valid Social Media platform.")