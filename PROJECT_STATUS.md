# PROJECT STATUS: VI-Translate Web Conversion & Deployment

## Tổng quan dự án
- **Gốc**: Repo `VI-Translate` (ứng dụng Desktop Python dùng `tkinter`, core xử lý PDF nặng dựa trên `pdf2zh`, `pymupdf`, `onnxruntime`, `opencv-python`).
- **Mục tiêu**: Phân tích & chuyển đổi thành Web App và triển khai trên hạ tầng miễn phí.

## Kiến trúc và Hệ thống triển khai (Đã quyết định)
- **Hệ thống Hosting**: **Hugging Face Spaces (Free Tier)**. 
- **Lý do**: Đây là hệ thống miễn phí duy nhất cung cấp đủ tài nguyên RAM (16GB RAM, 2 vCPU) cho các thư viện AI/ML nặng (`onnxruntime`, `opencv`) để nhận diện layout PDF. Vercel, Render (Free), Koyeb đều giới hạn ở mức 250MB-512MB RAM, chắc chắn sẽ gây lỗi Out of Memory.
- **Kiến trúc**:
  - Backend: **FastAPI** (`web/main.py`) bọc hàm `pdf2zh.translate` thành API endpoint `/api/translate`.
  - Frontend: **HTML/JS/CSS** thuần (`web/static/index.html`) được serve trực tiếp từ FastAPI để tránh lỗi CORS.
  - Deployment: **Docker** (`Dockerfile`) xây dựng môi trường Python 3.10 và các dependency hệ thống cho OpenCV (libGL...).

## Tiến độ
- [x] Scrape & clone repo VI-Translate.
- [x] Phân tích kiến trúc codebase và phát hiện các giới hạn phần cứng của thư viện AI.
- [x] Đề xuất Hugging Face Spaces làm nền tảng hosting miễn phí.
- [x] Triển khai code Web App:
  - Tạo `web/static/index.html` (Giao diện Frontend kéo thả file).
  - Tạo `web/main.py` (Backend FastAPI gọi core pdf2zh).
  - Tạo `Dockerfile` chuẩn bị cấu hình môi trường deploy lên Hugging Face.

## Bước tiếp theo (Dành cho User)
User chỉ cần tạo một Space mới (loại Docker) trên **Hugging Face**, sau đó Push toàn bộ source code này lên Space là ứng dụng sẽ tự động build và chạy trực tuyến.
