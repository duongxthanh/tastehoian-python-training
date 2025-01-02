from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import csv


def get_google_reviews(google_url, review_limit):
    driver = webdriver.Chrome()
    driver.set_window_size(1200, 800)

    try:
        # Truy cập vào URL
        driver.get(google_url)
        time.sleep(5)

        # Kiểm tra tiêu đề địa điểm
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, '.Lhccdd div')
            title = title_element.text.strip()  # Lấy tên địa điểm
            print(f"Đang trích xuất đánh giá từ: {title}")
        except Exception as e:
            print("Không tìm thấy địa điểm. Kiểm tra lại URL.")
            return  # Nếu không tìm thấy tiêu đề, dừng chương trình

        # Bấm vào nút 'Mới nhất' nếu có
        try:
            newest_button = driver.find_element(By.CSS_SELECTOR, '[data-sort-id="newestFirst"]')
            if newest_button.is_displayed():
                newest_button.click()
                time.sleep(2)  # Đợi trang cập nhật
                print("Đã chọn sắp xếp theo 'Mới nhất'.")
        except Exception:
            print("Không tìm thấy nút 'Mới nhất'. Tiếp tục trích xuất.")

        # Tìm phần tử scrollable trong popup đánh giá
        scrollable_element = driver.find_element(By.CLASS_NAME, 'review-dialog-list')

        # Lưu trữ dữ liệu đánh giá
        comment_data = []
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

        while len(comment_data) < review_limit:
            # Cuộn xuống cuối
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
            time.sleep(2)

            # Xử lý và bấm tất cả các nút "Thêm" cho đến khi không còn nút nào chưa bấm
            while True:
                more_buttons = scrollable_element.find_elements(By.CLASS_NAME, "review-more-link")
                buttons_clicked = 0  # Đếm số lượng nút đã bấm trong vòng lặp này
                for more_button in more_buttons:
                    try:
                        if more_button.is_displayed() and more_button.get_attribute("aria-expanded") == "false":
                            driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", more_button)
                            time.sleep(1)
                            more_button.click()
                            buttons_clicked += 1
                            time.sleep(1)
                    except Exception:
                        continue
                if buttons_clicked == 0:  # Dừng vòng lặp khi không còn nút nào chưa bấm
                    break

            # Xử lý dữ liệu đánh giá
            comments = scrollable_element.find_elements(By.CLASS_NAME, "jxjCjc")
            for comment in comments[len(comment_data):]:
                if len(comment_data) >= review_limit:  # Dừng khi đủ số lượng
                    break
                try:
                    author = comment.find_element(By.CLASS_NAME, "TSUbDb").text
                    role = comment.find_element(By.CLASS_NAME, "QV3IV").text.strip() if comment.find_elements(By.CLASS_NAME, "QV3IV") else "N/A"
                    rating_element = comment.find_element(By.CLASS_NAME, "lTi8oc")
                    rating = rating_element.get_attribute("aria-label")
                    # rating_value = re.search(r"(\d,\d|\d)", rating).group(1) if rating else "N/A"
                    rating_value = re.search(r"(\d+)", rating).group(1) if rating else "N/A"
                    time_element = comment.find_element(By.CLASS_NAME, "dehysf")
                    time_posted = time_element.text if time_element else "N/A"

                    # Nội dung đánh giá
                    try:
                        span_element = comment.find_element(By.XPATH, './/span[@data-expandable-section=""]')
                        visible_text = span_element.text.strip()
                        visible_text = re.sub(r'(\s*\|\s*|Đồ ăn:\s*\d/\d|Dịch vụ:\s*\d/\d|Bầu không khí:\s*\d/\d)', '', visible_text).strip().strip()
                        if not visible_text:
                            visible_text = "N/A"
                    except Exception:
                        visible_text = "N/A"

                    # Trích xuất thông tin thêm (Ăn tại chỗ, Bữa trưa, Giá)
                    additional_info = "N/A"
                    try:
                        additional_info_element = comment.find_element(By.CLASS_NAME, "PV7e7")
                        additional_info_parts = additional_info_element.find_elements(By.TAG_NAME, "span")
                        additional_info = " ".join([part.text for part in additional_info_parts]) if additional_info_parts else "N/A"
                    except Exception:
                        additional_info = "N/A"

                    # Chấm điểm chi tiết (Đồ ăn, Dịch vụ, Bầu không khí)
                    food_score = "N/A"
                    service_score = "N/A"
                    atmosphere_score = "N/A"
                    recommended_dishes = "N/A"

                    try:
                        detail_section = comment.find_element(By.CLASS_NAME, "k8MTF")
                        scores = detail_section.find_elements(By.TAG_NAME, "span")
                        for score in scores:
                            text = score.text.strip()
                            if "Đồ ăn" in text:
                                food_score = re.search(r"(\d+)", text).group(1) if re.search(r"(\d/\d)",
                                                                                               text) else "N/A"
                            elif "Dịch vụ" in text:
                                service_score = re.search(r"(\d+)", text).group(1) if re.search(r"(\d/\d)",
                                                                                                  text) else "N/A"
                            elif "Bầu không khí" in text:
                                atmosphere_score = re.search(r"(\d+)", text).group(1) if re.search(r"(\d/\d)",
                                                                                                     text) else "N/A"
                            elif "Những món ăn đề xuất" in text:
                                recommended_dishes = text.replace("Những món ăn đề xuất", "").strip()
                    except Exception:
                        pass

                    # Trích xuất lịch sử đánh giá
                    review_history = "N/A"
                    try:
                        review_history_element = comment.find_element(By.CLASS_NAME, "A503be")
                        review_history_text = review_history_element.text

                        # Kiểm tra nếu có cả đánh giá và ảnh
                        review_history_match = re.search(r"(\d+) đánh giá\s*(?:·\s*(\d+) ảnh)?", review_history_text)
                        if review_history_match:
                            reviews_count = review_history_match.group(1)
                            photos_count = review_history_match.group(2) if review_history_match.group(2) else "0"
                            review_history = f"{reviews_count} đánh giá, {photos_count} ảnh"
                        else:
                            # Trường hợp chỉ có ảnh
                            photo_only_match = re.search(r"(\d+) ảnh", review_history_text)
                            if photo_only_match:
                                photos_count = photo_only_match.group(1)
                                review_history = f"0 đánh giá, {photos_count} ảnh"
                    except Exception:
                        review_history = "N/A"

                    # Thêm dữ liệu vào danh sách
                    comment_data.append((len(comment_data) + 1, author, role, rating_value, time_posted, visible_text, food_score, service_score, atmosphere_score, recommended_dishes, additional_info, review_history))
                except Exception as e:
                    print(f"Lỗi xử lý đánh giá: {e}")

            # Dừng cuộn nếu không có nội dung mới
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
            if new_height == last_height:
                break
            last_height = new_height

        # In dữ liệu ra console
        print("\n--- Google Reviews ---\n")
        for review in comment_data:
            print(f"{review[0]}. {review[1]} ({review[2]}) (Rating: {review[3]}, Time: {review[4]}): {review[5]} | Food: {review[6]} | Service: {review[7]} | Atmosphere: {review[8]} | Recommended Dishes: {review[9]} | Additional Info: {review[10]} | Review History: {review[11]}")

        # Lưu dữ liệu vào file CSV
        valid_filename = re.sub(r'[\\/*?:"<>|]', "_", title).replace(" ", "_")
        filename = f"{valid_filename}_reviews.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Author", "Role", "Rating", "Time Posted", "Content", "Food Score", "Service Score", "Atmosphere Score", "Recommended Dishes", "Additional Info", "Review History"])
            writer.writerows(comment_data)

        print(f"Dữ liệu đánh giá đã được lưu vào {filename}.")
    finally:
        driver.quit()


# Nhập link Google Reviews
google_url = input("Nhập link Google Reviews: ")
review_limit = int(input("Nhập số lượng review muốn trích xuất: "))
get_google_reviews(google_url, review_limit)
