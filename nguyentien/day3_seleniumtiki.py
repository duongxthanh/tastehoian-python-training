from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

# Khởi động trình duyệt
driver = webdriver.Chrome()
driver.get(
    "https://tiki.vn/binh-giu-nhiet-locknlock-metro-drive-lhc4277s-650ml-kem-ong-hut-va-co-rua-p180378151.html?spid=180378153")

# Chờ trang tải
wait = WebDriverWait(driver, 10)


# Hàm cuộn trang
def scroll_to_load_comments():
    scroll_pause_time = 2  # Thời gian tạm dừng giữa các lần cuộn
    for _ in range(5):  # Cuộn xuống 5 lần
        driver.execute_script("window.scrollTo(0, 3200);")
        time.sleep(scroll_pause_time)


# Tạo file CSV nếu chưa tồn tại
if not os.path.exists('comments.csv'):
    with open('comments.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tên', 'Thời gian bình luận', 'Bình luận', 'Số sao'])

try:
    while True:
        scroll_to_load_comments()

        # Tìm tất cả bình luận trên trang
        comments = driver.find_elements(By.CSS_SELECTOR, ".review-comment")

        # Đọc dữ liệu từng bình luận
        new_data = []
        for comment in comments:
            try:
                name = comment.find_element(By.CSS_SELECTOR, ".review-comment__user-name").text
                time_comment = comment.find_element(By.CSS_SELECTOR,
                                                    ".review-comment__created-date > span:nth-of-type(1)").text
                review = comment.find_element(By.CSS_SELECTOR, ".review-comment__content").text

                # Lấy số sao từ img
                stars = comment.find_elements(By.CSS_SELECTOR, ".review-comment__rating > span > img")
                filled_stars = sum('efd76e1d41c00ad8ebb7287c66b559fd.png' in img.get_attribute('src') for img in stars)

                new_data.append((name, time_comment, review, filled_stars))

                print(f"{name} | {time_comment} | {review} | {filled_stars} sao")

            except Exception as e:
                print(f"Lỗi khi lấy dữ liệu bình luận: {e}")

        # Lưu vào CSV, loại bỏ trùng lặp
        existing_data = set()
        if os.path.exists('comments.csv'):
            with open('comments.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Bỏ qua dòng tiêu đề
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

        print(f"Đã thêm {new_count} bình luận mới vào file 'comments.csv'.")

        # Kiểm tra nút "Next" để chuyển trang
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
            if "disabled" in next_button.get_attribute("class"):
                print("Đã tới trang cuối cùng.")
                break
            next_button.click()
            time.sleep(3)  # Chờ trang tiếp theo tải xong
        except Exception as e:
            print("Không tìm thấy nút 'Next'. Dừng lặp.")
            break

except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")

finally:
    driver.quit()