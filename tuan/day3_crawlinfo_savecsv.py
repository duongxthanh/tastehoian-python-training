import csv
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Declare browser
driver = webdriver.Chrome()

# Open URL
driver.get("https://www.lazada.vn/dien-thoai-di-dong/?rating=1")
sleep(5)  # Sleep for a fixed 5 seconds

# Scroll to the bottom of the page to load all items
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)  # Fixed sleep of 2 seconds for scrolling
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_to_bottom()
sleep(3)  # Sleep for a fixed 3 seconds after scrolling

# ================================ GET link/title
elems = driver.find_elements(By.CSS_SELECTOR, ".RfADt [href]")
titles = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]

# Limit to 5 products
links = links[:5]

# ============================ GET INFORMATION OF ALL ITEMS
def scroll_to_comments():
    """Scroll down to the comments section."""
    for _ in range(5):  # Scroll a few times to ensure comments load
        driver.execute_script("window.scrollBy(0, 500);")
        sleep(2)  # Fixed sleep of 2 seconds for scrolling
    sleep(3)  # Sleep for a fixed 3 seconds after scrolling

def getDetailItems(link):
    driver.get(link)
    sleep(5)  # Fixed sleep for 5 seconds to allow the page to load
    scroll_to_comments()

    count = 1
    max_pages = 5  # Limit to 5 pages
    data = []

    while count <= max_pages:
        try:
            print(f"Crawl Page {count}")
            # Get comments, content, and ratings (star rating with <img>)
            elems_name = driver.find_elements(By.CSS_SELECTOR, ".middle")
            elems_content = driver.find_elements(By.CSS_SELECTOR, ".item-content .content")
            elems_rating = driver.find_elements(By.CSS_SELECTOR, ".container-star .star")
            elems_likeCount = driver.find_elements(By.CSS_SELECTOR, ".item-content .bottom .left .left-content")

            for name, content, rating, like in zip(elems_name, elems_content, elems_rating, elems_likeCount):
                # Get the number of stars (ratings) based on the number of <img class="star">
                num_stars = len(rating.find_elements(By.CSS_SELECTOR, "img.star"))
                data.append({
                    "link_item": link,
                    "name_comment": name.text,
                    "content_comment": content.text,
                    "star_rating": num_stars,  # Store the number of stars (rating)
                    "like_count": like.text
                })

            # Find and click the "Next" button
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".next-btn.next-btn-normal.next-btn-medium.next-btn-item.next")
                    )
                )
                next_button.click()
                print("Clicked on Next button.")
                sleep(2)  # Fixed sleep of 2 seconds after clicking next
            except (TimeoutException, NoSuchElementException):
                print("No Next button or timeout. Stopping pagination.")
                break

            # Close potential pop-ups
            try:
                close_btn = driver.find_element(By.XPATH, "//div[@class='popup-close']")
                close_btn.click()
                print("Clicked on popup close button.")
                sleep(2)  # Fixed sleep of 2 seconds after closing popup
            except NoSuchElementException:
                print("No popup to close.")
            count += 1
        except Exception as e:
            print(f"Error occurred: {e}")
            break

    return data

# Collect details from all links
all_data = []
for link in links:
    try:
        data = getDetailItems(link)
        all_data.extend(data)
    except Exception as e:
        print(f"Failed to process link {link}: {e}")

# Save data to CSV
output_path = "D:\\Pythonnnnn\\Quoctuan_labone\\tuan\\lazada_reviews.csv"
with open(output_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["link_item", "name_comment", "content_comment", "star_rating", "like_count"])
    writer.writeheader()
    writer.writerows(all_data)

print(f"Data saved to {output_path}")
driver.quit()
