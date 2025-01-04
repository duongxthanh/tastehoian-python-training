from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
import os
import re

# Cấu hình trình duyệt Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Mở trình duyệt
driver = webdriver.Chrome(options=options)
url = "https://www.google.com/search?q=cargo+club+cafe+%26+restaurant&lrd=0x31420e7e7b3bf0b5:0xea5248e85709aec3,1,,,"
driver.get(url)
time.sleep(3)  # Đợi trang tải hoàn toàn

# Cuộn xuống để tải thêm bình luận
try:
    scrollable_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'review-dialog-list'))
    )

    for _ in range(5):  # Tăng số lần nếu cần tải nhiều bình luận hơn
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
        time.sleep(2)

except TimeoutException:
    print("Không tìm thấy phần tử có thể cuộn.")

# Tạo file CSV nếu chưa tồn tại
if not os.path.exists('comments.csv'):
    with open('comments.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Tên',
            'Thời gian bình luận',
            'Bình luận',
            'Số sao đánh giá',
            'Danh hiệu',
            'Số lượng review & Ảnh',  # Cột mới
            'Điểm Đồ ăn',
            'Điểm Dịch vụ',
            'Điểm Bầu không khí',
            'Recommend food'
        ])

try:
    # Lấy tất cả bình luận
    comments = driver.find_elements(By.CSS_SELECTOR, ".jxjCjc")
    new_data = []

    for comment in comments:
        try:
            # Mở rộng nội dung nếu có nút "Xem thêm"
            try:
                load_more_button = comment.find_element(By.CSS_SELECTOR, ".review-more-link")
                if load_more_button.is_displayed():
                    load_more_button.click()
                    time.sleep(1)
            except NoSuchElementException:
                pass  # Không có nút "Xem thêm"

            # Lấy thông tin từ bình luận
            name = comment.find_element(By.CSS_SELECTOR, ".TSUbDb").text if comment.find_elements(By.CSS_SELECTOR,
                                                                                                  ".TSUbDb") else "N/A"
            time_comment = comment.find_element(By.CSS_SELECTOR, ".PuaHbe").text if comment.find_elements(
                By.CSS_SELECTOR, ".PuaHbe") else "N/A"
            review = comment.find_element(By.CSS_SELECTOR, ".Jtu6Td").text if comment.find_elements(By.CSS_SELECTOR,
                                                                                                    ".Jtu6Td") else "N/A"
            title = comment.find_element(By.CSS_SELECTOR, ".QV3IV").text if comment.find_elements(By.CSS_SELECTOR,
                                                                                                  ".QV3IV") else "N/A"

            # Lấy số sao
            try:
                star_element = comment.find_element(By.CSS_SELECTOR, "span.lTi8oc")
                star_class = star_element.get_attribute("aria-label")
                star_match = re.search(r"(\d(?:,\d)?)", star_class).group(1) if star_class else "N/A"
            except NoSuchElementException:
                star_match = "N/A"

            # Lấy thông tin số lượng review & ảnh
            try:
                review_photo_info = comment.find_element(By.CSS_SELECTOR, ".A503be").text
                # Dùng regex để gộp thông tin đánh giá và ảnh thành 1 chuỗi
                review_count_match = re.search(r"(\d[\d,.]*) đánh giá", review_photo_info)
                photo_count_match = re.search(r"(\d[\d,.]*) ảnh", review_photo_info)

                review_count = review_count_match.group(1) if review_count_match else "N/A"
                photo_count = photo_count_match.group(1) if photo_count_match else "N/A"
                review_photo_combined = f"{review_count} đánh giá · {photo_count} ảnh"

            except NoSuchElementException:
                review_photo_combined = "N/A"

            # Lấy thông tin chi tiết về Đồ ăn, Dịch vụ, Bầu không khí
            try:
                detailed_ratings = comment.find_element(By.CSS_SELECTOR, '.k8MTF').text
                food_rating = re.search(r'Đồ ăn:\s*(\d/\d)', detailed_ratings).group(1) if re.search(
                    r'Đồ ăn:\s*(\d/\d)', detailed_ratings) else "N/A"
                service_rating = re.search(r'Dịch vụ:\s*(\d/\d)', detailed_ratings).group(1) if re.search(
                    r'Dịch vụ:\s*(\d/\d)', detailed_ratings) else "N/A"
                atmosphere_rating = re.search(r'Bầu không khí:\s*(\d/\d)', detailed_ratings).group(1) if re.search(
                    r'Bầu không khí:\s*(\d/\d)', detailed_ratings) else "N/A"
            except NoSuchElementException:
                food_rating = "N/A"
                service_rating = "N/A"
                atmosphere_rating = "N/A"

            # Lấy Recommend food
            try:
                recommend_food = comment.find_element(By.CSS_SELECTOR,
                                                      ".k8MTF span:last-child").text if comment.find_elements(
                    By.CSS_SELECTOR, ".k8MTF span:last-child") else "N/A"
            except NoSuchElementException:
                recommend_food = "N/A"

            new_data.append((name, time_comment, review, star_match, title, review_photo_combined, food_rating,
                             service_rating, atmosphere_rating, recommend_food))
            print(
                f"{name} | {title} | {time_comment} | {review} | {star_match} | {review_photo_combined} | {food_rating} | {service_rating} | {atmosphere_rating} | {recommend_food}")

        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu từ một bình luận: {e}")

    # Kiểm tra và ghi vào CSV
    existing_data = set()
    if os.path.exists('comments.csv'):
        with open('comments.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                existing_data.add(tuple(row))

    with open('comments.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        new_count = 0
        for entry in new_data:
            if entry not in existing_data:
                writer.writerow(entry)
                existing_data.add(entry)
                new_count += 1

    print(f" Đã thêm {new_count} bình luận mới vào file 'comments.csv'.")

except Exception as e:
    print(f" Đã xảy ra lỗi: {e}")

finally:
    driver.quit()
