import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set Pandas options to left-align all columns
# pd.set_option('display.colheader_justify', 'left')  # Căn chỉnh tiêu đề cột sang trái
# pd.set_option('display.justify', 'left')  # Căn chỉnh các giá trị cột sang trái

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver: WebDriver = webdriver.Chrome(options=chrome_options)

# Open the URL
driver.get("https://fptshop.com.vn/ctkm/hotsale")

# Wait for page elements to load (use WebDriverWait instead of sleep)
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

# ================================ GET link/title
# Wait for the product cards to be visible
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ProductCard_cardTitle__HlwIo [href]")))

elems = driver.find_elements(By.CSS_SELECTOR, ".ProductCard_cardTitle__HlwIo [href]")
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]

# ================================ GET price
# Wait for price elements to be visible
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Price_currentPrice__PBYcv")))

elems_price = driver.find_elements(By.CSS_SELECTOR, ".Price_currentPrice__PBYcv")
price = [elem_price.text for elem_price in elems_price]

# ================================ Combine data into DataFrame
df1 = pd.DataFrame(list(zip(title, price, links)), columns=['title', 'price', 'link_item'])
df1['index_'] = np.arange(1, len(df1) + 1)

# ================================ Export to CSV
df1.to_csv('products_hot_sale.csv', index=False)

# Print the DataFrame to verify
print(df1.to_string())

# Optionally, display the first few rows in the console
df1.head()

# Close the browser after scraping
driver.quit()
