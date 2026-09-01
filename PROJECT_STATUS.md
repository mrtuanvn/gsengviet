# PROJECT STATUS: VI-Translate Web Conversion & Deployment

## Tổng quan dự án
- **Gốc**: Repo `VI-Translate` (chuyển đổi thành Web App chạy trên Hugging Face Spaces).
- **GitHub**: `https://github.com/mrtuanvn/gsengviet`
- **Hugging Face Space**: `https://huggingface.co/spaces/tuanipad/GSEngViet`

## Tiến độ
- [x] Chuyển đổi mã nguồn VI-Translate sang kiến trúc FastAPI + Gradio Blank Space (`app.py`, `packages.txt`).
- [x] Đẩy toàn bộ dự án lên GitHub `mrtuanvn/gsengviet`.
- [x] Đã cài đặt `git-lfs` và cấu hình `.gitattributes` xử lý file nhị phân (`*.png`, `*.ttf`, `*.onnx`) cho Hugging Face.
- [x] Cập nhật script tự động đồng bộ deploy: `deploy_hf.sh`.

## Bước tiếp theo (Dành cho User)
Chạy lại script `bash deploy_hf.sh` để đẩy code sang Hugging Face Space.
