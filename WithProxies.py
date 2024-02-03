from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from time import sleep

# Load proxies from file
with open('valid_proxies.txt', 'r') as file:
    proxies = file.read().split("\n")

# Create an iterator for the proxy list
proxy_cycle = iter(proxies)

# Function to get the next proxy from the cycle
def get_next_proxy():
    return next(proxy_cycle)

options = Options()
options.add_experimental_option("detach", True)

# Function to create a webdriver instance with a specified proxy
def create_webdriver(proxy):
    options.add_argument(f'--proxy-server={proxy}')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

website = "https://fameswap.com/browse-youtube-accounts-for-sale?v=1704742726"
names = []
subscribed = []
prices = []
listed_dates = []
descriptions = []

for _ in range(len(proxies)):
    proxy = get_next_proxy()
    driver = create_webdriver(proxy)

    try:
        driver.get(website)
    except TimeoutException:
        print(f"Proxy: {proxy} - Page load timed out")
        driver.quit()
        continue

    elements = driver.find_elements("xpath", "/html/body/div/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[1]/a")

    for element in elements:
        name = element.text
        link = element.get_attribute("href")

        # Open the link in a new tab with the specified proxy
        driver.execute_script(f"window.open('{link}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])

        # Your scraping logic here

        # Close the current tab and switch back to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Introduce a delay to avoid rapid requests
        sleep(3)

    # Close the main browser window
    driver.quit()
