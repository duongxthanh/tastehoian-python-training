from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import csv
import os


# Hàm trích xuất dữ liệu Google Reviews từ popup
def get_google_reviews(google_url):
    driver = webdriver.Chrome()
    driver.set_window_size(1200, 800)

    try:
        # Truy cập vào URL
        driver.get(google_url)
        time.sleep(5)

        # Kiểm tra tính hợp lệ của link (kiểm tra tiêu đề)
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, '.Lhccdd div')
            title = title_element.text.strip()  # Lấy tên địa điểm
            print(f"Đang trích xuất đánh giá từ: {title}")
        except Exception as e:
            print("Không tìm thấy địa điểm. Kiểm tra lại URL.")
            return  # Nếu không tìm thấy tiêu đề, dừng chương trình

        # Bấm vào nút 'Mới nhất' nếu cần
        # Tìm và bấm vào nút 'Mới nhất'
        newest_button = driver.find_element(By.CSS_SELECTOR, '[data-sort-id="newestFirst"]')
        if newest_button.is_displayed():
            newest_button.click()  # Bấm nút 'Mới nhất'
            time.sleep(2)  # Đợi trang cập nhật
            print("Đã chọn sắp xếp theo 'Mới nhất'.")


        # Trích xuất tên địa điểm từ tiêu đề
        title_element = driver.find_element(By.CLASS_NAME, "Lhccdd")
        title = title_element.find_element(By.TAG_NAME, "div").text  # Lấy tên địa điểm (cái đầu tiên)

        # Lọc tên file, loại bỏ các ký tự không hợp lệ
        valid_filename = re.sub(r'[\\/*?:"<>|]', "_", title)  # Thay thế các ký tự không hợp lệ bằng "_"
        valid_filename = valid_filename.replace(" ", "_")  # Thay thế dấu cách bằng dấu gạch dưới
        filename = f"{valid_filename}_reviews.csv"  # Đặt tên file

        # Tìm phần tử scrollable trong popup đánh giá
        scrollable_element = driver.find_element(By.CLASS_NAME, 'review-dialog-list')

        # Bấm nút "Thêm" ở lần tải đầu tiên
        initial_more_buttons = scrollable_element.find_elements(By.CLASS_NAME, "review-more-link")
        for more_button in initial_more_buttons:
            try:
                if more_button.is_displayed() and more_button.get_attribute("aria-expanded") == "false":
                    driver.execute_script("arguments[0].scrollIntoView();", more_button)  # Cuộn đến nút
                    time.sleep(1)
                    more_button.click()  # Nhấn nút "Thêm"
                    time.sleep(1)
            except Exception as e:
                print(f"Lỗi khi bấm nút 'Thêm' lần đầu: {e}")
                continue

        # Cuộn và bấm nút "Thêm" để tải thêm đánh giá
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
        while True:
            # Cuộn xuống cuối
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
            time.sleep(1)

            # Kiểm tra và bấm tất cả các nút "Thêm"
            more_buttons = scrollable_element.find_elements(By.CLASS_NAME, "review-more-link")
            for more_button in more_buttons:
                try:
                    if more_button.is_displayed() and more_button.get_attribute("aria-expanded") == "false":
                        driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
                        time.sleep(1)

                        # Kiểm tra nếu nút không bị che khuất
                        if more_button.is_displayed():
                            more_button.click()
                            time.sleep(1)
                        else:
                            # Nếu nút vẫn bị che khuất, thử cuộn lại lên trên để làm nó hiển thị
                            driver.execute_script("window.scrollBy(0, -300);")
                            time.sleep(1)
                            driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
                            time.sleep(1)
                            more_button.click()
                            time.sleep(1)
                except Exception as e:
                    print(f"Lỗi khi bấm nút 'Thêm': {e}")
                    continue

            # Kiểm tra nếu không còn nội dung mới để tải
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
            if new_height == last_height:
                break
            last_height = new_height

        # Xử lý dữ liệu đánh giá
        comments = driver.find_elements(By.CLASS_NAME, "jxjCjc")
        comment_data = []
        for index, comment in enumerate(comments, start=1):
            try:
                author = comment.find_element(By.CLASS_NAME, "TSUbDb").text
                rating_element = comment.find_element(By.CLASS_NAME, "lTi8oc")
                rating = rating_element.get_attribute("aria-label")
                rating_value = re.search(r"(\d,\d|\d)", rating).group(1) if rating else "N/A"
                time_element = comment.find_element(By.CLASS_NAME, "dehysf")
                time_posted = time_element.text if time_element else "N/A"
                # span_element = comment.find_element(By.XPATH, './/span[@data-expandable-section=""]')
                # visible_text = span_element.text
                try:
                    span_element = comment.find_element(By.XPATH, './/span[@data-expandable-section=""]')
                    visible_text = span_element.text
                except Exception:
                    visible_text = "No content"  # Gán giá trị mặc định nếu không có nội dung
                comment_data.append((index, author, rating_value, time_posted, visible_text))
            except Exception as e:
                print(f"Lỗi xử lý đánh giá: {e}")

        # In dữ liệu ra console
        print("\n--- Google Reviews ---\n")
        for index, author, rating, time_posted, content in comment_data:
            print(f"{index}. {author} (Rating: {rating}, Time: {time_posted}): {content}")

        # Lưu dữ liệu vào file CSV với tên địa điểm
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Author", "Rating", "Time Posted", "Content"])
            writer.writerows(comment_data)

        print(f"Dữ liệu đánh giá đã được lưu vào {filename}.")

    finally:
        driver.quit()


# Nhập link Google Reviews
google_url = input("Nhập link Google Reviews: ")
get_google_reviews(google_url)
