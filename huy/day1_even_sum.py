# Tính tổng các số chẵn từ 1 đến 100

def sum_even_numbers():
    total = 0
    for number in range(2, 101, 2):  # Bắt đầu từ 2, bước nhảy là 2
        total += number
    return total

# Gọi hàm và in kết quả
result = sum_even_numbers()
print("[Huyhq] Tổng các số chẵn từ 1 đến 100 là:", result)