import subprocess
import http.server
import socketserver
import os

PORT = 8501
DIRECTORY = "."  # تغییرات مربوط به دایرکتوری که کد استریم‌لیت شما در اون قرار داره

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"  # درخواست‌های اصلی به index.html هدایت می‌شود
        return super().do_GET()

def run_streamlit_app():
    # این تابع برای راه‌اندازی استریم‌لیت است
    subprocess.run(["streamlit", "run", "your_streamlit_app.py"])  # جایگزین با نام فایل استریم‌لیت شما

# راه‌اندازی سرور HTTP
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    # شروع اجرای اپلیکیشن استریم‌لیت به صورت جداگانه
    run_streamlit_app()
    httpd.serve_forever()
