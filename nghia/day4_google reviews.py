from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import csv

def extract_google_reviews(url, max_reviews):
    browser = webdriver.Chrome()
    browser.maximize_window()

    try:
        browser.get(url)
        time.sleep(5)

        reviews_section = browser.find_element(By.CLASS_NAME, 'review-dialog-list')

        while True:
            prev_scroll_position = browser.execute_script("return arguments[0].scrollTop", reviews_section)
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", reviews_section)
            time.sleep(1)
            current_scroll_position = browser.execute_script("return arguments[0].scrollTop", reviews_section)
            if current_scroll_position == prev_scroll_position:
                break

        reviews = browser.find_elements(By.CLASS_NAME, "jxjCjc")[:max_reviews]
        review_data = []

        for idx, review in enumerate(reviews, 1):
            try:
                reviewer = review.find_element(By.CLASS_NAME, "TSUbDb").text
                rating = re.search(r"\d(\.\d)?", review.find_element(By.CLASS_NAME, "lTi8oc").get_attribute("aria-label")).group()
                time_posted = review.find_element(By.CLASS_NAME, "dehysf").text
                content = review.find_element(By.XPATH, './/span[@data-expandable-section=""]').text

                try:
                    role = review.find_element(By.CLASS_NAME, "QV3IV").text
                except:
                    role = "No role"

                review_data.append((idx, reviewer, rating, time_posted, role, content))
            except:
                print(f"Error processing review {idx}.")

        with open("google_reviews.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Reviewer", "Rating", "Time", "Role", "Content"])
            writer.writerows(review_data)

        print("Saved reviews to google_reviews.csv.")

    finally:
        browser.quit()

# Example usage
google_review_url = "https://www.google.com/search?q=morning+glory+countryside&oq=morning+glory+countryside&gs_lcrp=EgZjaHJvbWUqCggAEAAY4wIYgAQyCggAEAAY4wIYgAQyDQgBEC4YrwEYxwEYgAQyCAgCEAAYFhgeMggIAxAAGBYYHjIICAQQABgWGB4yCAgFEAAYFhgeMggIBhAAGBYYHjIICAcQABgWGB4yCAgIEAAYFhgeMggICRAAGBYYHtIBCDU2ODdqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#lrd=0x31420f437ac49863:0x80c5d65a4320e118,1,,,,"
review_limit = 50
extract_google_reviews(google_review_url, review_limit)