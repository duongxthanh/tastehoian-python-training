from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
import re

# Configure Chrome options to start in maximized mode
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)  # Use appropriate driver for your browser
driver.get(
    "https://www.google.com/search?q=cargo+club+cafe+%26+restaurant&sca_esv=43387c1e70511b19&sxsrf=ADLYWILKNopWnK7cF4Q6BpMT4zGg7RA_Cg%3A1735354151728&ei=J2dvZ-CJLI_T2roPyIir8Qs&gs_ssp=eJwFwUsKgCAQAFDa1hVauKmt4y_NI3SLUUaFosAUOn7vjRPPXLR0bsUVGPwCnxJaAlmyQYUEwXj4CI3UjpyxsCNFdcwRa35YvHpgEROxlVV6G_aKd_sByt0Y_A&oq=cargo&gs_lp=Egxnd3Mtd2l6LXNlcnAiBWNhcmdvKgIIADILEC4YgAQYxwEYrwEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMgsQLhiABBjHARivATIFEAAYgAQyBRAAGIAEMgUQABiABDIIEC4YgAQYywFIjDFQohtY-SVwCHgAkAECmAGEAaABvgeqAQMxLje4AQPIAQD4AQGYAg6gAsIGwgIOEC4YgAQYsAMYxwEYrwHCAgkQABiwAxgHGB7CAgcQABiwAxgewgIJEAAYsAMYChgewgIKECMYgAQYJxiKBcICBBAjGCfCAgoQABiABBhDGIoFwgINEAAYgAQYsQMYQxiKBcICCxAAGIAEGLEDGIMBwgIOEC4YgAQYsQMYgwEYigXCAgUQLhiABMICEhAuGIAEGNEDGEMYxwEYigUYCsICCBAAGIAEGLEDwgIIEC4YgAQYsQPCAgQQABgDwgIEEC4YA5gDAIgGAZAGCpIHAzguNqAHllc&sclient=gws-wiz-serp#lrd=0x31420e7e7b3bf0b5:0xea5248e85709aec3,1,,,,"
)
# Allow the page to load
time.sleep(3)
scrollable_element = driver.find_element(By.CLASS_NAME, 'review-dialog-list')

# Scroll to load more reviews within the scrollable element
for _ in range(10):  # Adjust range as needed
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
    time.sleep(2)
# Tạo file CSV nếu chưa tồn tại
if not os.path.exists('comments.csv'):
    with open('comments.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tên', 'Thời gian bình luận', 'Bình luận', 'Số sao đánh giá'])

try:


    # Tìm tất cả bình luận trên trang
    comments = driver.find_elements(By.CSS_SELECTOR, ".jxjCjc")

    # Đọc dữ liệu từng bình luận
    new_data = []
    for comment in comments:
        try:
            load_more_button = comment.find_element(By.CSS_SELECTOR, ".review-more-link")
            if load_more_button.is_displayed():
                load_more_button.click()
                time.sleep(1)  # Đợi nội dung tải sau khi click
        except:
            pass  # Bỏ qua nếu không tìm thấy hoặc không thể click vào nút "Xem thêm"
        try:

            name = comment.find_element(By.CSS_SELECTOR, ".TSUbDb").text
            time_comment = comment.find_element(By.CSS_SELECTOR, ".PuaHbe").text
            review = comment.find_element(By.CSS_SELECTOR, ".Jtu6Td").text
            try:
                star_element = comment.find_element(By.CSS_SELECTOR, "span.lTi8oc")
                star_class = star_element.get_attribute("aria-label")
                star_match = re.search(r"(\d,\d)", star_class).group(1) if star_class else "N/A" # Cập nhật regex nếu cần


            except Exception as e:
                print("Không thể click vào nút:", e)
                stars = "Không rõ"
                print(f"Lỗi khi lấy số sao: {e}")



            new_data.append((name, time_comment, review , star_match))
            print(f"{name} | {time_comment} | {review} | {star_match}")

        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu bình luận: {e}")

    existing_data = set()
    if os.path.exists('comments.csv'):
        with open('comments.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Bỏ qua dòng tiêu đề
            for row in reader:
                existing_data.add(tuple(row))

    with open('comments.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        new_count = 0
        for entry in new_data:
            if entry not in existing_data:
                writer.writerow(entry)
                existing_data.add(entry)
                new_count += 1

    print(f"Đã thêm {new_count} bình luận mới vào file 'comments.csv'.")

except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")

finally:
    driver.quit()
