import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

'''Code that uses Selenium to headlessly open a URL and scroll to the bottom of a url and counts the number of 
advertising calls being made. Note this is not a perfect solution and the literature seems to sugges that routing
all traffic through a proxy is the best way to get a true count of the number of ad calls being made.
However,this does get us down the road and we could potentially use this to determine our own thresholds.
Tweaking the time delay between scrolls could also appears to help catch more ad calls.'''

# URL of the home page to analyze
url = "https://news24.com"

# Configure headless Chrome options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')
chrome_service = Service("chromedriver.exe") #path to chromedriver here

# Set a user agent to mimic a non-headless browser
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 " \
             "Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

# Create a new headless Chrome instance

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Load the URL and wait for page to fully render
driver.get(url)

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Set the initial scroll position and scroll step
current_position = 0
scroll_step = 500

total_height = driver.execute_script("return document.body.scrollHeight")

# Scroll through the page from top to bottom
while current_position < total_height:
    # Scroll down by the scroll step
    driver.execute_script(f"window.scrollTo(0, {current_position});")

    # Wait for a short period to allow the page to load as you scroll
    time.sleep(2)

    # Update the scroll position
    current_position += scroll_step

    # Update the total height in case new content was loaded while scrolling
    total_height = driver.execute_script("return document.body.scrollHeight")



# Get a list of all requests made by the page
requests = driver.execute_script("return window.performance.getEntries()")


with open('adhostnames.txt', 'r') as f:
    ad_domains = f.read().splitlines()

# extract the domains
ad_domains = [url.split("//")[-1].split("/")[0].split(".")[-2] for url in ad_domains]

# Filter the requests to find the ad requests
ad_requests = [r for r in requests if (domain.split("//")[-1].split("/")[0].split(".")[-2] in r["name"] for domain in ad_domains)]

# Count the number of ad requests
num_ads = len(ad_requests)

print("Number of ad requests:", num_ads)

driver.quit()
