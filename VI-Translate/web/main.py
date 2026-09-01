import os
import shutil
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VI-Translate Web API")

# Serve static files (HTML/JS/CSS)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="static")

def cleanup_temp_dir(dir_path: str):
    """Xóa thư mục tạm sau khi xử lý xong"""
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            logger.info(f"Cleaned up temp directory: {dir_path}")
    except Exception as e:
        logger.error(f"Error cleaning up {dir_path}: {e}")

try:
    import spaces
    gpu_decorator = spaces.GPU
except ImportError:
    def gpu_decorator(func):
        return func

@app.post("/api/translate")
@gpu_decorator
async def translate_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    lang_in: str = Form("en"),
    lang_out: str = Form("vi")
):
    if not file.filename.lower().endswith('.pdf'):
        return JSONResponse(status_code=400, content={"detail": "Chỉ hỗ trợ định dạng PDF."})
        
    try:
        from pdf2zh import translate
    except ImportError:
        return JSONResponse(status_code=500, content={"detail": "Không tìm thấy thư viện pdf2zh. Hãy chắc chắn đã cài đặt core app."})

    # Tạo thư mục tạm để chứa file
    temp_dir = tempfile.mkdtemp(prefix="vitranslate_")
    input_pdf_path = os.path.join(temp_dir, "input.pdf")
    
    try:
        # Lưu file upload
        with open(input_pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        logger.info(f"Start translating {file.filename} from {lang_in} to {lang_out}")
        
        # Gọi hàm translate của pdf2zh
        # pdf2zh.translate nhận params: files, lang_in, lang_out, output_dir...
        # Lưu ý: output_dir mặc định là thư mục chứa file pdf gốc
        # Nếu translate() trả về file path thì tốt, nếu không ta phải check thư mục
        translated_files = translate(
            files=[input_pdf_path],
            lang_in=lang_in,
            lang_out=lang_out,
            output=temp_dir
        )
        
        if not translated_files:
            # pdf2zh có thể append suffix "_zh" hoặc "_vi" hoặc tên gì đó. 
            # Lấy file pdf khác với input.pdf trong temp_dir
            out_files = [f for f in os.listdir(temp_dir) if f.endswith('.pdf') and f != "input.pdf"]
            if out_files:
                output_pdf_path = os.path.join(temp_dir, out_files[0])
            else:
                raise Exception("Không tìm thấy file kết quả sau khi dịch.")
        else:
            output_pdf_path = translated_files[0]
            
        # Lên lịch xóa thư mục tạm sau khi response file
        background_tasks.add_task(cleanup_temp_dir, temp_dir)
        
        # Trả về file đã dịch
        return FileResponse(
            path=output_pdf_path, 
            filename=f"translated_{file.filename}",
            media_type="application/pdf"
        )
        
    except Exception as e:
        cleanup_temp_dir(temp_dir)
        logger.error(f"Translation failed: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.get("/")
def root():
    # Redirect to UI
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
