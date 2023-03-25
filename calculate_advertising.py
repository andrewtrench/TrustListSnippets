from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from PIL import Image
import io
import time

'''Code that uses Selenium to headlessly open a URL and scroll to the bottom of a url and takes a screenshot of the 
entire page and then calculates the total area of advertising versus the size of the web page.
Note: The chrome driver must be installed and the path to the driver must be specified in the code below.
Including the code here because it is interesting appraoch but big challenge is getting the the ads to fire in headless mode.
The full screen imagegrab part of it could be useful for one stage of the funnel where screengrabs are suggested'''

# URL of the home page to analyze
url = "http://gossipinfo.com.ng"

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

# Get the size of the visible viewport
width = driver.execute_script("return Math.max(document.documentElement.clientWidth, window.innerWidth || 0)")
height = driver.execute_script("return Math.max(document.documentElement.clientHeight, window.innerHeight || 0)")
# Get the size of the entire page, including content below the fold
total_height = driver.execute_script("return document.body.scrollHeight")

# Set the initial scroll position and scroll step
current_position = 0
scroll_step = 500

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
# Get the size of the entire page, including content below the fold
total_width = driver.execute_script("return Math.max(document.documentElement.scrollWidth, document.body.scrollWidth, document.documentElement.clientWidth, window.innerWidth || 0)")
#total_height = driver.execute_script("return Math.max(document.documentElement.scrollHeight, document.body.scrollHeight, document.documentElement.clientHeight, window.innerHeight || 0)")

# Resize the browser window to fit the entire page
driver.set_window_size(total_width, total_height)

# Take a screenshot of the entire page and convert it to a PIL Image object
screenshot = driver.get_screenshot_as_png()
image = Image.open(io.BytesIO(screenshot))
image.show()

# Calculate the total area of the entire page
total_area = total_width * total_height
print(total_area)
# Loop through all <img> and <iframe> tags and calculate the area of each one
ad_area = 0
for element in driver.find_elements(By.XPATH, '//img|//iframe'):
    # Get the location and size of the element
    location = element.location
    size = element.size
    print (size['width'], size['height'])

    # Calculate the area of the element
    try:
        element_area = size['width'] * size['height']

        # Convert the location and size to pixel coordinates
        x = location['x']
        y = location['y']
        w = size['width']
        h = size['height']
        box = (x, y, x+w, y+h)

        # Crop the screenshot to the element's bounding box and convert it to a PIL Image object
        element_image = image.crop(box)

        # Calculate the average brightness of the element's image
        element_brightness = sum(element_image.convert('L').getdata()) / (w * h * 255)

        # If the element's brightness is above a certain threshold, count it as an advertisement
        if element_brightness > 0.5:
            ad_area += element_area
    except ZeroDivisionError:
        pass

# Calculate the ratio of advertising area to total page area
ad_ratio = ad_area / total_area * 100

# Print the result
print(f"The advertising intensity on {url} is {ad_ratio:.2f}%")
