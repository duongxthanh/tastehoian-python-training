import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

# Declare browser
driver = webdriver.Chrome()

# Open URL
driver.get("https://fptshop.com.vn/ctkm/hotsale")
sleep(random.randint(5, 10))

# ================================ GET link/title
elems = driver.find_elements(By.CSS_SELECTOR, ".ProductCard_cardTitle__HlwIo [href]")
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]
#
# # ================================ GET price
elems_price = driver.find_elements(By.CSS_SELECTOR, ".Price_currentPrice__PBYcv")
len(elems_price)
price = [elem_price.text for elem_price in elems_price]

df1 = pd.DataFrame(list(zip(title, price, links)), columns=['title', 'price', 'link_item'])
df1['index_'] = np.arange(1, len(df1) + 1)

# Print the DataFrame to see the output
print(df1)

# If you want to see it in PyCharm's data viewer
df1.head()  #