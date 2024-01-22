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
#login = "https://fameswap.com/auth/login?v=1705842671"
website = "https://fameswap.com/browse"

i = 0
social_media = []
names = []
subscribed = []
prices = []
listed_dates = []
descriptions = []
category = []

#driver.get(login)
#sleep(450)
driver.get(website)
number_of_pages = driver.find_element("xpath", "/html/body/div/div/div[3]/div[2]/div/div[3]/nav/ul/li[12]/a")
while (i < 1):

    elements = driver.find_elements("xpath", "/html/body/div/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[1]/a")

    element = elements[1]

    name = element.text
    link = element.get_attribute("href")

    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)

    social_media_element = driver.find_element("xpath", "/html/body/div[1]/div/div[1]/h1/span")
    category_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[4]/a")
    subscribed_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[1]")
    price_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[2]")
    listed_date_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[3]")
    description_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[4]/p")
    sleep(2)

    names.append(name)
    category.append(category_element.accessible_name)
    subscribed.append(subscribed_element.text)
    prices.append(price_element.text)
    listed_dates.append(listed_date_element.text)
    descriptions.append(description_element.text)

    if 'Youtube' in social_media_element.text:
        social_media.append("Youtube")
    elif 'Twitter':
        social_media.append("Twitter")
    else:
        social_media.append("Tiktok")

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    sleep(5)
    driver.find_element("xpath", "//ul[@class='pagination']/li/a[@rel='next']").click()
    i = i + 1

    client = MongoClient()

try:
    db = client.WebScraping
    collection = db.WebScraping
    scraped_data_list = []
    for j in range(len(names)):
        entry = {
            "Name": names[j],
            "Social Media": social_media[j],
            "Subscribers": subscribed[j],
            "Price": prices[j],
            "Date Listed": listed_dates[j],
            "Description": descriptions[j],
            "Category": category[j]
        }
        scraped_data_list.append(entry)

    # Insert multiple documents at once
    collection.insert_many(scraped_data_list)

except Exception as e:
    print(f"Error Occurred: {e}")

finally:
    # Close the MongoDB connection
    client.close()
    print("Connection Closed")