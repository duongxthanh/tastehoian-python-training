def sum_even_number():
    # Sử dụng vòng lặp và điều kiện để tính tổng các số chẵn
    even_total = 0
    for number in range(1, 101):
        if number % 2 == 0:
            even_total += number

    return even_total


# In kết quả
result = sum_even_number()
print("Tổng các số chẵn từ 1 đến 100 là: ",result)