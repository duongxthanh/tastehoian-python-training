import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Đọc dữ liệu
df = pd.read_csv("Morning_Glory_Lounge_Bar_&_Restaurant_reviews.csv")

# Tạo figure với 3 subplot
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# --- 1. Word Cloud ---
content_text = " ".join(df["Content"].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(content_text)
axes[0].imshow(wordcloud, interpolation='bilinear')
axes[0].axis("off")
axes[0].set_title("Word Cloud từ nội dung đánh giá")

# --- 2. Histogram ---
sns.histplot(df["Rating"], bins=5, kde=True, color='skyblue', ax=axes[1])
axes[1].set_xlabel("Rating")
axes[1].set_ylabel("Số lượng đánh giá")
axes[1].set_title("Phân bố Rating")
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

# --- 3. Pie Chart ---
score_means = df[["Food Score", "Service Score", "Atmosphere Score"]].mean()
axes[2].pie(score_means, labels=score_means.index, autopct='%1.1f%%', colors=["#ff9999", "#66b3ff", "#99ff99"])
axes[2].set_title("Tỷ lệ trung bình của Food, Service, Atmosphere")

# Hiển thị tất cả biểu đồ
plt.tight_layout()
plt.show()
