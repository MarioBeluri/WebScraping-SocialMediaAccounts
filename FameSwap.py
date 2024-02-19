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
login = "https://fameswap.com/auth/login"
website = "https://fameswap.com/browse?v=1706219067&social=3%2C4%2C5"

i = 0
URLs = []
names = []
seller = []
trust_score = []
seller_nationality = []
social_media = []
address = []
followers = []
prices = []
descriptions = []
listed_dates = []
categories = []
monthly_incomes = []
monthly_expenses = []
likes = []
posts = []
comments = []
views = []
revenue = []
rate = []
verified = []

driver.get(login)
sleep(30)
driver.get(website)
sleep(5)
number_of_pages = driver.find_element("xpath", "/html/body/div/div/div[3]/div[2]/div/div[3]/nav/ul/li[12]/a")

while (i < int(number_of_pages.accessible_name) - 1):
    elements = driver.find_elements("xpath", "/html/body/div/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[1]/a")

    for element in elements:
        name = element.text
        link = element.get_attribute("href")
        original_window = driver.current_window_handle
        URLs.append(link)

        driver.switch_to.new_window('tab')
        driver.get(link)
        sleep(2)
        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break

        try:
            ul_element = driver.find_element(By.CLASS_NAME, "list-unstyled")
            statistics = ul_element.find_elements(By.TAG_NAME,"li")
            for statistic in statistics:
                text = statistic.text
                if 'Views' in text:
                    views.append(text.split(":")[-1].strip())
                elif 'Verified' in text:
                    verified.append(text.split(":")[-1].strip())
                elif 'Posts' in text:
                    posts.append(text.split(":")[-1].strip())
                elif 'Likes' in text:
                    likes.append(text.split(":")[-1].strip())
                elif 'Comments' in text:
                    comments.append(text.split(":")[-1].strip())
                elif 'Rate' in text:
                    rate.append(text.split(":")[-1].strip())
                elif 'Revenue' in text:
                    revenue.append(text.split(":")[-1].strip())
        except:
            posts.append("None")
            views.append("None")
            verified.append("None")
            likes.append("None")
            comments.append("None")
            rate.append("None")
            revenue.append("None")

        seller = driver.find_element(By.XPATH,'//div[@class="panel-body"]/strong/a').text
        trust_score = driver.find_element(By.XPATH,
            '//div[@class="panel-body"]//small/strong').text
        seller_nationality_element = driver.find_elements(By.XPATH, '//p[@class="text-muted"]/small')[1]
        seller_nationality.append(seller_nationality_element.text.strip())

        category_element = driver.find_element("xpath",
                                               "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[4]/a")
        subscribed_element = driver.find_element("xpath",
                                                 "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[1]")
        price_element = driver.find_element("xpath",
                                            "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[2]")
        listed_date_element = driver.find_element("xpath",
                                                  "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[3]")
        description_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[4]/p")
        sleep(2)

        names.append(name)
        categories.append(category_element.accessible_name)
        followers.append(subscribed_element.text)
        prices.append(price_element.text)
        listed_dates.append(listed_date_element.text)
        descriptions.append(description_element.text)
        social_media_element = driver.find_element("xpath", "/html/body/div[1]/div/div[1]/h1/span")

        if 'Youtube' in social_media_element.text:
            social_media.append("Youtube")
        elif 'Twitter':
            social_media.append("Twitter")
        else:
            social_media.append("Tiktok")

        driver.close()
        driver.switch_to.window(original_window)
        sleep(2)
    driver.find_element("xpath", "//ul[@class='pagination']/li/a[@rel='next']").click()
    i += 1

# try:
#     client = MongoClient()
#     db = client.WebScraping
#     collection = db.WebScraping
#     scraped_data = {
#         "Name" : names,
#         "Social Media" : social_media,
#         "Followers" : followers,
#         "Price" : prices,
#         "Date Listed" : listed_dates,
#         "Description" : descriptions,
#         "Category" : categories
#     }
#     collection.insert_one(scraped_data)
# except:
#     print("Error Occured")
# finally:
#     client.close()
#     print("Conenction Closed")