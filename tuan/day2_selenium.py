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
driver.get("https://www.lazada.vn/dien-thoai-di-dong/?page=1&spm=a2o4n.home.cate_1.1.1905e182tGDwoM")
sleep(random.randint(5, 10))

# ================================ GET link/title
elems = driver.find_elements(By.CSS_SELECTOR, ".RfADt [href]")
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]
#
# # ================================ GET price
elems_price = driver.find_elements(By.CSS_SELECTOR, ".aBrP0")
len(elems_price)
price = [elem_price.text for elem_price in elems_price]

df1 = pd.DataFrame(list(zip(title, price, links)), columns=['title', 'price', 'link_item'])
df1['index_'] = np.arange(1, len(df1) + 1)

# Print the DataFrame to see the output
print(df1)

# If you want to see it in PyCharm's data viewer
df1.head()  #

