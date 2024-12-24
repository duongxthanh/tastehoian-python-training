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

    # Cuộn trang để đảm bảo các phần tử tải đầy đủ
    for _ in range(5):  # Cuộn xuống 5 lần
        driver.execute_script("window.scrollTo(0, 3200);")
        time.sleep(scroll_pause_time)

    # Tạo danh sách để lưu bình luận, tên và thời gian
    comment_list = []
    name_list = []
    time_list = []

    # Tìm và nhấn các nút chuyển trang bình luận
    while True:
        # Lấy bình luận hiện tại
        comments = driver.find_elements(By.CSS_SELECTOR, ".review-comment__content")
        names = driver.find_elements(By.CSS_SELECTOR, ".review-comment__user-name")
        times = driver.find_elements(By.CSS_SELECTOR, ".review-comment__created-date span")

        # Lưu dữ liệu
        comment_list = [comment.text for comment in comments]
        name_list = [username.text for username in names]
        time_list = [usernametime.text for usernametime in times]
        print(
            f"Tìm thấy {len(comments)} bình luận, {len(names)} tên, {len(times) if 'times' in locals() else 0} thời gian.")

        # Tìm nút "Next" và nhấn nếu có
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".customer-reviews__pagination ul.loVmKB a.next svg")))
            next_button.click()
            time.sleep(2)  # Chờ trang tiếp theo tải
        except Exception as e:
            print("Không tìm thấy nút 'Next' hoặc đã đến trang cuối.")
            break

    # Hiển thị số lượng dữ liệu
    print(f"Tìm thấy {len(comment_list)} bình luận, {len(name_list)} tên, {len(time_list)} thời gian.")

    # In dữ liệu ra màn hình
    for i, (review, adminname, admintime) in enumerate(zip(comment_list, name_list, time_list), 1):
        print(f"{i}. {adminname} ({admintime}): {review}")

    # Lưu dữ liệu vào file CSV
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