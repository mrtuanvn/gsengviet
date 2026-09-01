import os
import shutil
import tempfile
import gradio as gr
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import spaces

@spaces.GPU
def translate_pdf_gradio(file_path, lang_in, lang_out):
    if not file_path:
        raise gr.Error("Vui lòng chọn một file PDF.")
    
    try:
        from pdf2zh import translate
        from pdf2zh.doclayout import OnnxModel
        model = OnnxModel.load_available()
    except ImportError:
        raise gr.Error("Không tìm thấy thư viện pdf2zh. Hãy chắc chắn đã cài đặt core app.")

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp(prefix="vitranslate_")
    
    try:
        logger.info(f"Start translating {file_path} from {lang_in} to {lang_out}")
        
        translated_files = translate(
            files=[file_path],
            lang_in=lang_in if lang_in else "en",
            lang_out=lang_out if lang_out else "vi",
            output=temp_dir,
            service="google",
            model=model
        )
        
        if not translated_files:
            out_files = [f for f in os.listdir(temp_dir) if f.endswith('.pdf')]
            if out_files:
                output_pdf_path = os.path.join(temp_dir, out_files[0])
            else:
                raise gr.Error("Không tìm thấy file kết quả sau khi dịch.")
        else:
            output_pdf_path = translated_files[0]
            
        return output_pdf_path
        
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise gr.Error(f"Lỗi khi dịch: {str(e)}")

# Define the Gradio Blocks UI
with gr.Blocks(title="VI-Translate Web") as demo:
    gr.Markdown("# VI-Translate")
    gr.Markdown("Dịch PDF giữ nguyên bố cục sang Tiếng Việt (hỗ trợ bởi ZeroGPU).")
    
    with gr.Row():
        with gr.Column():
            pdf_file = gr.File(label="Chọn file PDF", file_types=[".pdf"])
            lang_in = gr.Textbox(label="Ngôn ngữ gốc (tùy chọn)", placeholder="Ví dụ: en", value="en")
            lang_out = gr.Textbox(label="Ngôn ngữ đích", value="vi")
            translate_btn = gr.Button("Bắt đầu Dịch", variant="primary")
            
        with gr.Column():
            output_file = gr.File(label="File kết quả")
            
    translate_btn.click(
        fn=translate_pdf_gradio,
        inputs=[pdf_file, lang_in, lang_out],
        outputs=output_file
    )

if __name__ == "__main__":
    demo.launch()
