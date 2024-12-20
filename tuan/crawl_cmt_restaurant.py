from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import re
Link_Ancient_Remedy ="https://www.google.com/search?q=restaurant+Hoi+An+Ancient+Remedy&rlz=1C1UEAD_enVN1087VN1087&oq=restaurant+Hoi+An+Ancient+Remedy&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yDQgCEAAYhgMYgAQYigUyDQgDEAAYhgMYgAQYigUyCggEEAAYgAQYogQyCggFEAAYogQYiQUyCggGEAAYgAQYogTSAQc0NTBqMGo5qAIAsAIB&sourceid=chrome&ie=UTF-8#lrd=0x31420f21fbbf7403:0x8da1a8c5d64e0a7d,1,,,,"
Link_Vegan ="https://www.google.com/search?q=v+vegan+-+vegan+cafe+%26+restaurant&sca_esv=ca11c9d49f096907&rlz=1C1UEAD_enVN1087VN1087&ei=04NvZ9OjKYqc0-kPyaXdyQg&ved=0ahUKEwiT2ZKq1cmKAxUKzjQHHclSN4kQ4dUDCBA&uact=5&oq=v+vegan+-+vegan+cafe+%26+restaurant&gs_lp=Egxnd3Mtd2l6LXNlcnAiIXYgdmVnYW4gLSB2ZWdhbiBjYWZlICYgcmVzdGF1cmFudDIIEAAYgAQYsAMyBxAAGLADGB4yCRAAGLADGAcYHjIJEAAYsAMYBxgeMgkQABiwAxgHGB4yCRAAGLADGAcYHjIHEAAYsAMYHjIOEAAYgAQYsAMYhgMYigUyDhAAGIAEGLADGIYDGIoFMg4QABiABBiwAxiGAxiKBUiAElAAWMgMcAJ4AJABAJgBAKABAKoBALgBA8gBAPgBAfgBApgCAqACEagCCsICFBAAGIAEGJECGLQCGIoFGOoC2AEBwgIaEC4YgAQYkQIYtAIYxwEYigUY6gIYrwHYAQHCAhoQABiABBi0AhjlAhi3AxiKBRjqAhiKA9gBAcICEBAAGAMYtAIY6gIYjwHYAQHCAhAQLhgDGLQCGOoCGI8B2AEBmAMK8QWNM6lhPMG_2YgGAZAGCroGBAgBGAeSBwEyoAcA&sclient=gws-wiz-serp"
url = Link_Ancient_Remedy
def extract_google_reviews(url, max_scrolls=100, scroll_pause=3):
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()
    driver.set_window_size(1200, 800)
    try:
        # Truy cập vào URL
        driver.get(url)
        time.sleep(3)  # Đợi trang tải
        # Kiểm tra và lấy tiêu đề
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, '.Lhccdd div')
            title = title_element.text.strip()
            print(f"Đang thu thập đánh giá từ: {title}")
        except Exception:
            print("Không thể xác định tiêu đề địa điểm. Vui lòng kiểm tra URL.")
            return
        # Tạo tên file
        valid_filename = title.translate(str.maketrans(' ', ' ', '\\/*?:"<>|'))
        filename = f"{valid_filename}.csv"
        # Tìm phần tử chứa danh sách đánh giá
        review_list = driver.find_element(By.CLASS_NAME, 'review-dialog-list')
        # Danh sách chứa dữ liệu đánh giá
        reviews_data = []
        # Cuộn tối đa số lần được chỉ định
        last_review_count = 0
        for scroll_count in range(max_scrolls):
            print(f"Đang cuộn lần thứ {scroll_count + 1}/{max_scrolls}...")
            # Lấy các đánh giá hiển thị hiện tại
            reviews = driver.find_elements(By.CLASS_NAME, 'jxjCjc')
            # Thu thập dữ liệu mới
            for review in reviews[last_review_count:]:
                try:
                    # Tác giả
                    author = review.find_element(By.CLASS_NAME, "TSUbDb").text
                    # Số sao
                    rating = review.find_element(By.CLASS_NAME, "lTi8oc").get_attribute("aria-label")
                    rating_value = re.search(r"\d+", rating).group(0) if rating else "N/A"
                    # Thời gian đăng
                    time_posted = review.find_element(By.CLASS_NAME, "dehysf").text
                    # Nội dung đánh giá
                    try:
                        content = review.find_element(By.XPATH, './/span[@data-expandable-section=""]').text
                    except Exception:
                        content = "Không có nội dung"

                    reviews_data.append((author, rating_value, time_posted, content))
                except Exception as e:
                    print(f"Lỗi khi xử lý một đánh giá: {e}")
                    continue
            last_review_count = len(reviews)  # Cập nhật số lượng đánh giá đã xử lý
            # Cuộn xuống cuối danh sách
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", review_list)
            time.sleep(scroll_pause)  # Đợi thêm dữ liệu tải
            # Kiểm tra nếu không còn nội dung mới để tải
            new_reviews = len(driver.find_elements(By.CLASS_NAME, 'jxjCjc'))
            if new_reviews == last_review_count:
                print("Không còn đánh giá mới để tải.")
                break
        # Lưu dữ liệu vào CSV
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Author", "Rating", "Time Posted", "Comment"])
            writer.writerows(reviews_data)

        print(f"Đã lưu dữ liệu đánh giá vào file: {filename}")
    except Exception as e:
        print(f"Lỗi tổng quát: {e}")
    finally:
        driver.quit()
extract_google_reviews(url)


