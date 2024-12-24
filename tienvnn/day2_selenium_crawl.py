from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import urllib.parse

def get_thegioididong_comments(product_url, output_file="comments.csv", max_pages=5):
    # Khởi tạo trình duyệt Chrome với Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # Bỏ qua sandbox nếu môi trường yêu cầu
    options.add_argument("--disable-dev-shm-usage")  # Giảm lỗi liên quan đến bộ nhớ chia sẻ
    driver = webdriver.Chrome(options=options)

    # Thiết lập kích thước cửa sổ trình duyệt
    driver.maximize_window()

    try:
        data = []
        for page in range(1, max_pages + 1):
            print(f"Đang xử lý trang {page}...")
            # Tạo URL cho từng trang
            parsed_url = urllib.parse.urlparse(product_url)
            query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
            query_params["page"] = page
            page_url = urllib.parse.urlunparse(parsed_url._replace(query=urllib.parse.urlencode(query_params)))

            driver.get(page_url)
            time.sleep(5)  # Đợi tải trang

            # Tìm các phần tử chứa thông tin đánh giá
            reviewers = driver.find_elements(By.XPATH, "//p[@class='cmt-top-name']")
            comments = driver.find_elements(By.XPATH, "//p[@class='cmt-txt']")
            stars_elements = driver.find_elements(By.XPATH, "//div[@class='cmt-top-star']")

            # Lấy dữ liệu từ các phần tử
            for reviewer, comment, stars_element in zip(reviewers, comments, stars_elements):
                # Đếm số lượng sao bằng cách đếm các thẻ <i> với lớp "iconcmt-starbuy"
                stars_count = len(stars_element.find_elements(By.XPATH, ".//i[contains(@class, 'iconcmt-starbuy')]"))
                entry = {
                    "Reviewer": reviewer.text,
                    "Comment": comment.text,
                    "Stars": stars_count
                }
                data.append(entry)
                # In dữ liệu ra console
                print(entry)

        # Lưu dữ liệu vào file CSV
        with open(output_file, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Reviewer", "Comment", "Stars"])
            writer.writeheader()
            writer.writerows(data)

        print(f"Đã lưu {len(data)} đánh giá vào file {output_file}.")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

    finally:
        # Đóng trình duyệt
        driver.quit()


# Nhập link sản phẩm Thegioididong
product_url = input("Nhập link sản phẩm Thegioididong: ")
get_thegioididong_comments(product_url)