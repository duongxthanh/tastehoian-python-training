from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Khởi động trình duyệt
driver = webdriver.Chrome()  # Đảm bảo bạn đã cài đặt ChromeDriver
driver.get("https://tiki.vn/binh-giu-nhiet-locknlock-metro-drive-lhc4277s-650ml-kem-ong-hut-va-co-rua-p180378151.html?spid=180378153")
# driver.set_window_size(1920, 1080)

# Chờ trang tải
wait = WebDriverWait(driver, 10)

# Cuộn trang và tải thêm bình luận
try:
    scroll_pause_time = 2  # Thời gian tạm dừng giữa các lần cuộn
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    # Cuộn trang 5 lần
    for _ in range(5):  # Cuộn xuống 5 lần
        driver.execute_script("window.scrollTo(0, 3200);")
        time.sleep(scroll_pause_time)

    # Tìm nút "Xem thêm" nếu có
    try:
        show_more_button = driver.find_elements(By.CSS_SELECTOR, " span .show-more-content")
        show_more_button.click()  # Nhấp vào nút "Xem thêm"
        time.sleep(2)  # Chờ 2 giây để tải bình luận
    except Exception as e:
        print("Không tìm thấy nút 'Xem thêm' hoặc không cần nhấn")

    # Lấy tất cả bình luận
    comments = driver.find_elements(By.CSS_SELECTOR, ".review-comment__content ")
    name = driver.find_elements(By.CSS_SELECTOR, ".review-comment__user-name")
    time = driver.find_elements(By.CSS_SELECTOR, ".review-comment__created-date span")
    comment_list = [comment.text for comment in comments]
    name_list = [username.text for username in name]
    time_list = [usernametime.text for usernametime in time]
    print(f"Tìm thấy {len(comments)} bình luận, {len(name)} tên, {len(time) if 'times' in locals() else 0} thời gian.")

    for i, (review, adminname,admintime) in enumerate(zip(comment_list, name_list,time_list), 1):
        print(f"{i}. {adminname}:{admintime}: {review}")

    with open('comments.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tên','thời gian bình luận','Bình luận'])
        for adminname, review in zip(name_list, comment_list):
            writer.writerow([adminname, admintime, review])

    print("Dữ liệu đã được lưu vào file 'comments.csv' thành công.")

except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")

finally:
    driver.quit()