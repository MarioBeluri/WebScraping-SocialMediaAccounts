from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

#options = Options()
#options.add_experimental_option("detach", True)
#driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = Driver(uc=True)
#login = "https://fameswap.com/auth/login?v=1705842671"
website = "https://fameswap.com/browse-youtube-accounts-for-sale?v=1703794243"

names = []
subscribed = []
prices = []
listed_dates = []
descriptions = []

#driver.get(login)
#sleep(450)
driver.get(website)
elements = driver.find_elements("xpath", "/html/body/div/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[1]/a")

for element in elements:
    name = element.text
    link = element.get_attribute("href")

    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)

    subscribed_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[1]")
    price_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[2]")
    listed_date_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/table/tbody/tr/td[3]")
    description_element = driver.find_element("xpath", "/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[4]/p")
    sleep(2)

    names.append(name)
    subscribed.append(subscribed_element.text)
    prices.append(price_element.text)
    listed_dates.append(listed_date_element.text)
    descriptions.append(description_element.text)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    sleep(5)


print(names)
print(subscribed)
print(prices)
print(listed_dates)
print(descriptions)
