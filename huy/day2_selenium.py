from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# Hàm để trích xuất bình luận, tên người bình luận, thời gian bình luận và số lượt thích
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

        # Tìm tất cả các phần tử cha chứa thông tin bình luận
        comment_containers = driver.find_elements(By.XPATH, "//ytd-comment-thread-renderer")

        # Lấy thông tin từ từng phần tử cha
        comment_data = []
        for index, container in enumerate(comment_containers, start=1):
            try:
                # Lấy tên người bình luận
                author_name = container.find_element(By.XPATH, ".//a[@id='author-text']//span").text.strip()

                # Lấy nội dung bình luận
                comment_text = container.find_element(By.XPATH, ".//yt-attributed-string[@id='content-text']").text.strip()

                # Lấy thời gian bình luận
                time_posted = container.find_element(By.XPATH, ".//span[@id='published-time-text']//a").text.strip()

                # Lấy số lượt thích
                like_count = container.find_element(By.XPATH, ".//span[@id='vote-count-middle']").text.strip()
                like_count = like_count if like_count else "0"  # Nếu không có số like, mặc định là "0"

                # Thêm thông tin vào danh sách
                comment_data.append((index, author_name, comment_text, time_posted, like_count))
            except Exception as e:
                # Nếu có lỗi khi lấy dữ liệu, bỏ qua phần tử đó
                print(f"Lỗi: {e}")
                continue

        # In dữ liệu ra console
        print("\n--- Bình luận trên YouTube ---\n")
        for index, author, comment, time_posted, likes in comment_data:
            print(f"{index}. {author} ({time_posted}, Likes: {likes}): {comment}")

        # Lưu dữ liệu vào file CSV
        with open("youtube_comments.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Author", "Comment", "Time Posted", "Likes"])
            writer.writerows(comment_data)

        return comment_data

    finally:
        # Đóng trình duyệt
        driver.quit()

# Nhập link video YouTube
video_url = input("Nhập link YouTube: ")
get_youtube_comments(video_url)
