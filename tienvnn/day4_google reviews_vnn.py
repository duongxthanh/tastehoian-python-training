from selenium import webdriver
from selenium.webdriver.common.by import By
import time  # Thư viện time này phải được import
import re  # Thêm import re nếu bạn sử dụng regex để xử lý chuỗi
import csv

def extract_reviews_from_google(url, max_reviews):
    browser = webdriver.Chrome()
    browser.set_window_size(1200, 800)

    try:
        browser.get(url)
        time.sleep(5)  # Đảm bảo import thư viện time để sử dụng sleep

        try:
            title_element = browser.find_element(By.CSS_SELECTOR, '.Lhccdd div')
            place_name = title_element.text.strip()
            print(f"Đang lấy đánh giá từ: {place_name}")
        except Exception:
            print("Không tìm thấy tên địa điểm. Vui lòng kiểm tra lại URL.")
            return

        reviews_section = browser.find_element(By.CLASS_NAME, 'review-dialog-list')

        load_more_buttons = reviews_section.find_elements(By.CLASS_NAME, "review-more-link")
        for button in load_more_buttons:
            if button.is_displayed() and button.get_attribute("aria-expanded") == "false":
                button.click()
                time.sleep(1)

        prev_height = browser.execute_script("return arguments[0].scrollHeight", reviews_section)
        while True:
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", reviews_section)
            time.sleep(1)

            load_more_buttons = reviews_section.find_elements(By.CLASS_NAME, "review-more-link")
            for button in load_more_buttons:
                if button.is_displayed() and button.get_attribute("aria-expanded") == "false":
                    button.click()
                    time.sleep(1)

            current_height = browser.execute_script("return arguments[0].scrollHeight", reviews_section)
            if current_height == prev_height:
                break
            prev_height = current_height

        review_elements = browser.find_elements(By.CLASS_NAME, "jxjCjc")
        review_data = []

        for idx, review in enumerate(review_elements, start=1):
            if idx > max_reviews:
                break
            try:
                reviewer = review.find_element(By.CLASS_NAME, "TSUbDb").text
                rating_elem = review.find_element(By.CLASS_NAME, "lTi8oc")
                rating = rating_elem.get_attribute("aria-label")
                rating_value = re.search(r"(\d,\d|\d)", rating).group(1) if rating else "N/A"
                time_posted_elem = review.find_element(By.CLASS_NAME, "dehysf")
                time_posted = time_posted_elem.text if time_posted_elem else "N/A"  # Đổi tên biến tránh xung đột

                try:
                    role_elem = review.find_element(By.CLASS_NAME, "QV3IV")
                    role = role_elem.text.strip()
                except Exception:
                    role = "No role"

                review_details = review.find_elements(By.CLASS_NAME, "Aohxlc")
                if len(review_details) >= 2:
                    review_count = re.search(r'\d+', review_details[0].text).group() if review_details[0].text else "0"
                    photo_count = re.search(r'\d+', review_details[1].text).group() if review_details[1].text else "0"
                else:
                    review_count, photo_count = "0", "0"

                try:
                    content_elem = review.find_element(By.XPATH, './/span[@data-expandable-section=""]')
                    content = content_elem.text
                except Exception:
                    content = "No content"

                review_data.append((idx, reviewer, rating_value, time_posted, role, review_count, photo_count, content))

            except Exception as e:
                print(f"Không thể xử lý đánh giá {idx}: {e}")

        print("\n--- Google Reviews ---\n")
        for idx, reviewer, rating, time_posted, role, reviews, photos, content in review_data:
            print(
                f"{idx}. {reviewer} (Rating: {rating}, Time: {time_posted}, Role: {role}, Reviews: {reviews}, Photos: {photos}): {content}")

        with open("google_reviews.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Index", "Author", "Rating", "Time Posted", "Role", "Review Count", "Photo Count", "Content"])
            writer.writerows(review_data)

        print("Đã lưu dữ liệu vào google_reviews.csv.")

    finally:
        browser.quit()


google_review_url = "https://www.google.com/search?q=the+waterfront+h%E1%BB%99i+an&sca_esv=80ab0116367e6cb1&ei=DzN2Z_fDJoan2roP1rLW8AI&gs_ssp=eJzj4tVP1zc0LM9KsTAqzMg2YLRSNagwNjQxMkgzSU41Tk00SEpJsjKoMDc2tUgxSDM3TUk1MDc1sPASL8lIVShPLEktSivKzytRyHi4e2amQmIeAJZwGSY&oq=The+Waterfront+Hoi+An&gs_lp=Egxnd3Mtd2l6LXNlcnAiFVRoZSBXYXRlcmZyb250IEhvaSBBbioCCAAyCxAuGIAEGMcBGK8BMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMgUQABjvBTIaEC4YgAQYxwEYrwEYlwUY3AQY3gQY4ATYAQFInBRQAFgAcAB4AJABAJgBbqABbqoBAzAuMbgBA8gBAPgBAvgBAZgCAqAC8xKYAwC6BgYIARABGBSSBwcwLjEuOC0xoAeOBg&sclient=gws-wiz-serp#lrd=0x31420f4ce3ea0bdb:0x7358d0f75de07508,1,,,,"
review_limit = 100

extract_reviews_from_google(google_review_url, review_limit)
