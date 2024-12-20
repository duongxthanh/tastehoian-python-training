from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Hàm để trích xuất comment từ YouTube
def get_youtube_comments(video_url):
    # Khởi chạy trình duyệt Chrome
    driver = webdriver.Chrome()

    # Thiết lập kích thước cửa sổ trình duyệt
    driver.set_window_size(400, 500)

    try:
        # Truy cập video YouTube
        driver.get(video_url)
        time.sleep(5)  # Đợi trang tải xong

        # Cuộn trang để tải các bình luận
        scroll_pause_time = 2  # Thời gian tạm dừng giữa các lần cuộn
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Cuộn xuống cuối trang
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(scroll_pause_time)

            # Kiểm tra xem đã cuộn tới cuối trang chưa
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Tìm các bình luận theo class
        #comments = driver.find_elements(By.CSS_SELECTOR, 'div#content yt-attributed-string span.yt-core-attributed-string')
        comments = driver.find_elements(By.XPATH, "//div[@id='content']//yt-attributed-string//span[@class='yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap']")
        comment_list = [comment.text for comment in comments]

        # In các bình luận ra console
        print("\n--- Bình luận trên YouTube ---\n")
        for i, comment in enumerate(comment_list, 1):
            print(f"{i}: {comment}")

        return comment_list

    finally:
        # Đóng trình duyệt
        driver.quit()

# Nhập link video YouTube
video_url = input("Nhập link YouTube: ")
get_youtube_comments(video_url)
