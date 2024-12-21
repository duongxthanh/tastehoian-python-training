from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import csv

# Configure Chrome options to start in maximized mode
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)  # Use appropriate driver for your browser
driver.get('https://www.google.com/search?q=Cargo+Club+Cafe+%26+Restaurant&sca_esv=b61b3658a3ed087d&sxsrf=ADLYWIKZLMoH2d-rTGHxhNrRb49RhD-XMQ%3A1733660865373&ei=wZBVZ87AFq_71e8P55zNuQs&ved=0ahUKEwiOpaqAlpiKAxWvffUHHWdOM7cQ4dUDCA8&uact=5&oq=Cargo+Club+Cafe+%26+Restaurant&gs_lp=Egxnd3Mtd2l6LXNlcnAiHENhcmdvIENsdWIgQ2FmZSAmIFJlc3RhdXJhbnQyBBAjGCcyBRAAGIAEMhEQLhiABBjHARjJAxjLARivATIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB5IxB1Q6RpYjhxwA3gAkAEAmAG5AaABrgOqAQMwLjO4AQPIAQD4AQGYAgSgAqQBwgIKEAAYsAMY1gQYR5gDAIgGAZAGB5IHAzMuMaAHiR0&sclient=gws-wiz-serp#lrd=0x31420e7e7b3bf0b5:0xea5248e85709aec3,1,,,,')

# Allow the page to load
time.sleep(5)

# Find the scrollable element with the class name 'review-dialog-list'
scrollable_element = driver.find_element(By.CLASS_NAME, 'review-dialog-list')

# Scroll to load more reviews within the scrollable element
for _ in range(5):  # Adjust range as needed
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
    time.sleep(2)

# Create or open the CSV file and write headers
with open('thanh\/reviews.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Author", "Rating", "Content"])  # Write the headers

    # Find and process each comment
    comments = driver.find_elements(By.CLASS_NAME, "jxjCjc")  # Use the correct class
    for comment in comments:
        try:
            # Extract author
            author = comment.find_element(By.CLASS_NAME, "TSUbDb").text

            # Extract rating
            rating_element = comment.find_element(By.CLASS_NAME, "lTi8oc")  # Find the span with class "lTi8oc"
            rating = rating_element.get_attribute("aria-label")  # Get the aria-label attribute value
            rating_value = re.search(r"(\d,\d)", rating).group(1) if rating else "N/A"

            # Extract comment content
            span_element = comment.find_element(By.XPATH, './/span[@data-expandable-section=""]')
            visible_text = span_element.text

            # Write the data to the CSV file
            writer.writerow([author, rating_value, visible_text])
        except Exception as e:
            print(f"Error processing comment: {e}")

# Close the browser
driver.quit()

print("Reviews have been saved to reviews.csv.")
