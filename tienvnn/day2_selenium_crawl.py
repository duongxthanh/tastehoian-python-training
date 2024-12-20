from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
# Hàm để trích xuất comment từ Thegioididong
def get_thegioididong_comments(product_url):
    # Khởi chạy trình duyệt Chrome với Selenium WebDriver
    driver = webdriver.Chrome()

    # Thiết lập kích thước cửa sổ trình duyệt
    driver.set_window_size(580, 470)  # Điều chỉnh theo nhu cầu

    try:
        # Truy cập trang sản phẩm
        driver.get(product_url)
        time.sleep(10)  # Đợi tải trang

        # Cuộn trang để tải các bình luận
        scroll_pause_time = 2  # Thời gian tạm dừng giữa các lần cuộn
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        # Tìm các bình luận
        comments = driver.find_elements(By.XPATH, "//p[@class='cmt-txt']")
        comment_list = [comment.text for comment in comments]

        # In các bình luận ra console
        print("\n--- Bình luận trên Thegioididong ---\n")
        for i, comment in enumerate(comment_list, 1):
            print(f"{i}: {comment}")

        return comment_list

    finally:
        # Đóng trình duyệt
        driver.quit()

# Nhập link sản phẩm Thegioididong
product_url = input("Nhập link sản phẩm Thegioididong: ")
get_thegioididong_comments(product_url)
