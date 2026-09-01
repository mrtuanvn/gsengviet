# PROJECT STATUS: VI-Translate Web Conversion & Deployment

## Tổng quan dự án
- **Gốc**: Repo `VI-Translate` (chuyển đổi thành Web App chạy trên Hugging Face Spaces).
- **GitHub**: `https://github.com/mrtuanvn/gsengviet`
- **Hugging Face Space**: `https://huggingface.co/spaces/tuanipad/GSEngViet`

## Tiến độ
- [x] Chuyển đổi mã nguồn VI-Translate sang kiến trúc FastAPI + Gradio Blank Space (`app.py`, `packages.txt`).
- [x] Đẩy toàn bộ dự án lên GitHub `mrtuanvn/gsengviet`.
- [x] Cấu hình `.gitattributes` và loại bỏ thư mục không cần thiết (`.github`) để đáp ứng quy định Git LFS / file nhị phân của Hugging Face.
- [x] Đẩy thành công mã nguồn lên Hugging Face Space `tuanipad/GSEngViet` (Push accepted).
- [x] Thêm đầy đủ YAML frontmatter (bao gồm `sdk_version`) vào VI-Translate/README.md để khắc phục lỗi cấu hình repo card của Hugging Face.

## Trạng thái hiện tại
Mã nguồn đã được tải lên Hugging Face Space thành công. Hugging Face đang tự động build và khởi chạy ứng dụng.
- [x] Sửa lỗi Build Error trên Hugging Face (cache miss) bằng cách làm sạch file `packages.txt`, do image cơ sở đã có sẵn các thư viện hệ thống cần thiết.
- [x] Sửa lỗi Dependency Conflict giữa `python-multipart` và `gradio` bằng cách cập nhật `python-multipart>=0.0.9` trong file `requirements.txt`.
- [x] ~~Sửa lỗi xung đột `huggingface_hub` với `gradio==4.44.1` và `babeldoc==0.2.33` bằng cách nâng cấp `sdk_version` lên `5.0.0` và gỡ pin `huggingface_hub<0.26`.~~ **Không đủ**: `gradio==5.0.0` vẫn import `HfFolder` từ `huggingface_hub` trong `gradio/oauth.py` (đã xác nhận qua log lỗi runtime thực tế sau khi deploy) → Space vẫn crash với `ImportError: cannot import name 'HfFolder'`.
- [x] Sửa dứt điểm lỗi `HfFolder`. Root cause thật: `babeldoc==0.2.33` yêu cầu `huggingface-hub>=0.27.0`, còn mọi bản `gradio<5.10.0` (đã kiểm chứng `4.44.1` và `5.0.0`, cả hai đều lỗi) import `HfFolder` — bị xóa khỏi `huggingface_hub>=0.26`. Hai ràng buộc mâu thuẫn trực tiếp, không có bản `huggingface_hub` nào thỏa cả hai. Đã tải `gradio/oauth.py` từ GitHub qua các tag để xác minh: `gradio@5.5.0` còn dùng `HfFolder`, `gradio@5.10.0` đã đổi sang `get_token()` và chỉ cần `huggingface-hub>=0.25.1` (thỏa mãn babeldoc).
  - Fix: nâng `sdk_version` trong `VI-Translate/README.md` lên `"5.10.0"`, không pin `huggingface_hub` nữa.
  - Đồng thời gỡ pin cứng `fastapi==0.104.1` / `uvicorn==0.24.0` trong `requirements.txt` — `app.py` đã là Gradio thuần, không import FastAPI/uvicorn trực tiếp, và `gradio==5.10.0` yêu cầu `fastapi>=0.115.2` (xung đột với pin cũ).
  - ⚠️ Đã có ít nhất 2 lần thay đổi bị ghi đè lẫn nhau giữa các phiên làm việc trên file `requirements.txt`/`README.md`/`PROJECT_STATUS.md` (commit `afdb1d5` xóa mất một fix trước đó dựa trên giả định chưa kiểm chứng bằng log thực tế). Trước khi đổi lại cấu hình gradio/huggingface_hub, hãy đọc kỹ mục này và `git log`/`git diff` để tránh lặp lại.

- [x] Sửa lỗi "Error: No API found" trên giao diện Hugging Face Spaces (do Gradio 5 Server-Side Rendering (SSR) gây ra với ZeroGPU/spaces) bằng cách thêm `ssr_mode=False` vào `demo.launch()` trong file `app.py`.
