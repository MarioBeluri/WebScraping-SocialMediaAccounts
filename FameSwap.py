from seleniumbase import Driver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from time import sleep
from utils.logging import logger as LOGGER

driver = Driver(uc=True)
client = MongoClient()
db = client.WebScraping
collection = db.FameSwap
login = "https://fameswap.com/auth/login"
website = "https://fameswap.com/browse?v=1706219067&social=3%2C4%2C5"

driver.get(login)
sleep(60)
driver.get(website)
sleep(5)
while True:
    elements = driver.find_elements("xpath", "/html/body/div/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[1]/a")

    for element in elements:
        name = element.text
        link = element.get_attribute("href")
        original_window = driver.current_window_handle
        URL= link

        driver.switch_to.new_window('tab')
        driver.get(link)
        sleep(5)
        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break

        try:
            posts = None
            view = None
            verified = None
            likes = None
            comments = None
            rate = None
            revenue = None
            dislikes = None

            ul_element = driver.find_element(By.CLASS_NAME, "list-unstyled")
            statistics = ul_element.find_elements(By.TAG_NAME,"li")
            for statistic in statistics:
                text = statistic.text
                if 'Views' in text:
                    view = int(text.split(":")[-1].strip().split()[0].replace(",", ""))
                elif 'Verified' in text:
                    verified = text.split(":")[-1].strip()
                elif 'Posts' in text:
                    posts = int(text.split(":")[-1].strip())
                elif 'Likes' in text:
                    likes = int(text.split(":")[-1].strip())
                elif 'Dislikes' in text:
                    dislikes = int(text.split(":")[-1].strip())
                elif 'Comments' in text:
                    comments = int(text.split(":")[-1].strip())
                elif 'Eng' in text:
                    rate = text.split(":")[-1].strip()
                elif 'Revenue' in text:
                    revenue = float(text.split(":")[-1].strip().replace("$", ""))
        except Exception as e:
            posts = None
            view = None
            verified = None
            likes = None
            comments = None
            rate = None
            revenue = None
            dislikes = None



        try:
            seller = driver.find_element(By.XPATH,'//div[@class="panel-body"]/strong/a').text
        except Exception as e:
            LOGGER.info("Error occurred while extracting seller information:", e)
            seller = None

        try:
            trust_score = int(driver.find_element(By.XPATH, '//div[@class="panel-body"]//small/strong').text.strip("()"))
        except Exception as e:
            LOGGER.info("Error occurred while extracting seller information:", e)
            trust_score = None

        try:
            seller_nationality_element = driver.find_elements(By.XPATH, '//p[@class="text-muted"]/small')[1]
            seller_nationality = seller_nationality_element.text.strip()
        except Exception as e:
            LOGGER.info("Error occurred while extracting seller information:", e)
            seller_nationality = None

        try:
            category_element = driver.find_element("xpath",
                                                   "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[4]/a")
            categorie = category_element.accessible_name
        except Exception as e:
            LOGGER.info("Error occurred while extracting category information:", e)
            categorie = None

        try:
            subscribed_element = driver.find_element("xpath",
                                                     "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[1]")
            follower = int(subscribed_element.text.replace(",", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting followers information:", e)
            follower = None

        try:
            price_element = driver.find_element("xpath",
                                                "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[2]")
            price = float(price_element.text.replace(",", ""))
        except Exception as e:
            LOGGER.info("Error occurred while extracting price information:", e)
            price = None

        try:
            listed_date_element = driver.find_element("xpath",
                                                      "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[3]")
            listed_date = listed_date_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting listed date information:", e)
            listed_date = None

        try:
            offer_paragraph = driver.find_element(By.XPATH, "//div[@class='panel-body']/p[contains(text(), 'best offer so far')]").text
            offer_best_amount = offer_paragraph.split()[0]
            offer_amount = float(offer_best_amount[1:])
        except Exception as e:
            LOGGER.info("Error occurred while extracting offer information:", e)
            offer_amount = None

        try:
            description_element = driver.find_element("xpath",
                                                      "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[4]/p")
            description = description_element.text
        except Exception as e:
            LOGGER.info("Error occurred while extracting description information:", e)
            description = None

        sleep(2)

        try:
            social_media_element = driver.find_element("xpath", "/html/body/div[1]/div/div[1]/h1/span")
            if 'Youtube' in social_media_element.text:
                social_media = "Youtube"
            elif 'Twitter' in social_media_element.text:
                social_media = "Twitter"
            else:
                social_media = "Tiktok"
        except Exception as e:
            LOGGER.info("Error occurred while extracting description information:", e)
            social_media = None

        try:
            entry_data = {
                    "url": URL,
                    "title": name,
                    "seller": seller,
                    "seller_nationality": seller_nationality,
                    "listed_date": listed_date,
                    "price": price,
                    "social_media": social_media,
                    "description": description,
                    "followers": follower,
                    "category": categorie,
                    "trust_score": trust_score,
                    "average_views": view,
                    "verified": verified,
                    "posts": posts,
                    "average_likes": likes,
                    "average_dislikes": dislikes,
                    "best_offer": offer_amount,
                    "average_comments": comments,
                    "revenue": revenue,
                    "rate": rate
                }
            collection.insert_one(entry_data)

        except Exception as e:
            LOGGER.info("Error Occurred:", e)
            client.close()
            LOGGER.info("Connection Closed")

        driver.close()
        driver.switch_to.window(original_window)
        sleep(2)
    try:
        next_page = driver.find_element("xpath", "//ul[@class='pagination']/li/a[@rel='next']")
        next_page.click()
        sleep(8)
    except:
        break

client.close()
LOGGER.info("Conenction Closed")
driver.quit()
LOGGER.info("Scraping finished")