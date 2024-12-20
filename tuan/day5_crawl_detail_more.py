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

        # Bấm vào nút 'Mới nhất' nếu có
        try:
            newest_button = driver.find_element(By.CSS_SELECTOR, '[data-sort-id="newestFirst"]')
            if newest_button.is_displayed():
                newest_button.click()
                time.sleep(2)  # Đợi trang cập nhật
                print("Đã chọn sắp xếp theo 'Mới nhất'.")
        except Exception:
            print("Không tìm thấy nút 'Mới nhất'. Tiếp tục trích xuất.")

        # Tạo tên file
        valid_filename = title.translate(str.maketrans(' ', ' ', '\\/*?:"<>|'))
        filename = f"{valid_filename}.csv"
        # Tìm phần tử chứa danh sách đánh giá
        review_list = driver.find_element(By.CLASS_NAME, 'review-dialog-list')
        # Danh sách chứa dữ liệu đánh giá
        reviews_data = []

        # Xử lý và bấm tất cả các nút "Thêm" cho đến khi không còn nút nào chưa bấm
        while True:
            more_buttons = driver.find_elements(By.CLASS_NAME, "review-more-link")
            buttons_clicked = 0  # Đếm số lượng nút đã bấm trong vòng lặp này
            for more_button in more_buttons:
                try:
                    if more_button.is_displayed() and more_button.get_attribute("aria-expanded") == "false":
                        driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", more_button)
                        time.sleep(1)
                        more_button.click()
                        buttons_clicked += 1
                        time.sleep(2)
                except Exception:
                    continue
            if buttons_clicked == 0:  # Dừng vòng lặp khi không còn nút nào chưa bấm
                break

        # Cuộn tối đa số lần được chỉ định và lấy dữ liệu đánh giá
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

                    # Lấy thông tin từ thẻ div có class 'PV7e7'
                    dining_info = driver.find_element(By.CLASS_NAME, 'PV7e7').find_elements(By.TAG_NAME, 'span')
                    if len(dining_info) >= 3:
                        dine_in = dining_info[0].text
                        meal_type = dining_info[2].text
                        price_range = dining_info[4].text
                    else:
                        dine_in = meal_type = price_range = "N/A"

                    # Lấy thông tin về điểm Food, Service, Atmosphere và Món ăn đề xuất
                    try:
                        # Tìm tất cả các thẻ có class `k8MTF`
                        review_details = review.find_elements(By.CLASS_NAME, 'k8MTF')
                        food, service, atmosphere, dish = "N/A", "N/A", "N/A", "N/A"

                        for detail in review_details:
                            detail_text = detail.get_attribute("innerHTML")  # Lấy nội dung HTML thô
                            print("Debug - Nội dung thô:", detail_text)  # In ra để kiểm tra cấu trúc

                            # Sử dụng các mẫu regex để trích xuất thông tin
                            food_rating = re.search(r"<b>Đồ ăn</b>:\s*(\d+)/5", detail_text)
                            service_rating = re.search(r"<b>Dịch vụ</b>:\s*(\d+)/5", detail_text)
                            atmosphere_rating = re.search(r"<b>Bầu không khí</b>:\s*(\d+)/5", detail_text)
                            # recommended_dish = re.search(r"<b>Recommended dishes</b>\s*([^<]+)", detail_text)

                            # Cập nhật giá trị nếu tìm thấy
                            if food_rating:
                                food = food_rating.group(1)
                            if service_rating:
                                service = service_rating.group(1)
                            if atmosphere_rating:
                                atmosphere = atmosphere_rating.group(1)
                            # if recommended_dish:
                            #     dish = recommended_dish.group(1).strip()
                    except Exception as e:
                        print(f"Lỗi khi xử lý thông tin chi tiết: {e}")
                        food, service, atmosphere, dish = "N/A", "N/A", "N/A", "N/A"

                    # Thêm vào danh sách dữ liệu đánh giá
                    reviews_data.append((author, rating_value, time_posted, content, dine_in, meal_type, price_range,
                                         food, service, atmosphere, dish))
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
            writer.writerow(
                ["Author", "Rating", "Time Posted", "Comment", "Dining Option", "Meal Type", "Price Range", "Food",
                 "Service", "Atmosphere", "Recommended Dish"])
            writer.writerows(reviews_data)

        print(f"Đã lưu dữ liệu đánh giá vào file: {filename}")
    except Exception as e:
        print(f"Lỗi tổng quát: {e}")
    finally:
        driver.quit()


# Gọi hàm với URL bạn muốn lấy đánh giá
extract_google_reviews(url)
