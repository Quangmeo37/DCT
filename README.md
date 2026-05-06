# 📸 DCT Image Compression

Ứng dụng nén ảnh sử dụng thuật toán **Discrete Cosine Transform (DCT)** – nền tảng của chuẩn JPEG.

---

## 🧠 Giới thiệu

Hệ thống được xây dựng nhằm thực hiện nén ảnh số dựa trên thuật toán **DCT (Discrete Cosine Transform)**.  
Mục tiêu là giảm kích thước lưu trữ của ảnh nhưng vẫn giữ chất lượng ở mức chấp nhận được.

Hệ thống hỗ trợ **ảnh màu (RGB)**, trong đó mỗi kênh màu (R, G, B) được xử lý độc lập, mô phỏng gần với các hệ thống nén ảnh thực tế.

---

## ⚙️ Chức năng chính

### 📂 Chọn ảnh đầu vào
- Người dùng chọn ảnh từ máy tính

### 🖼️ Hiển thị ảnh gốc
- Ảnh hiển thị đầy đủ màu sắc

### 🔄 Nén ảnh bằng DCT
Quy trình gồm:
- Chia ảnh thành các block **8x8**
- Áp dụng **DCT**
- **Lượng tử hóa**
- **IDCT** để tái tạo ảnh

### 📊 Hiển thị kết quả
- So sánh ảnh **trước và sau nén**

### 💾 Lưu ảnh
- Cho phép chọn **tên file** và **đường dẫn lưu**

---

