import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.show_upload_form()
        elif self.path.startswith('/download'):
            self.handle_download()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/upload':
            self.handle_upload()
        else:
            self.send_error(404, "File not found")

    def show_upload_form(self):
        files = os.listdir(UPLOAD_DIR)
        file_links = "\n".join(f'<li><a href="/download?file={f}">{f}</a></li>' for f in files)

        html = f"""
        <html>
        <head>
            <title>File Server</title>
            <style>
                body {{ font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f5f5f5; margin: 0; }}
                .container {{ width: 100%; max-width: 600px; text-align: center; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); }}
                h2 {{ color: #333; }}
                form {{ margin-bottom: 20px; }}
                input[type="file"] {{ display: block; margin: 10px auto; }}
                button {{ padding: 10px 20px; color: #fff; background-color: #007BFF; border: none; border-radius: 4px; cursor: pointer; }}
                button:hover {{ background-color: #0056b3; }}
                ul {{ list-style-type: none; padding: 0; }}
                li {{ padding: 8px; }}
                a {{ text-decoration: none; color: #007BFF; }}
                a:hover {{ text-decoration: underline; }}
                .footer {{ font-size: 0.8em; color: #666; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Upload a File</h2>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <button type="submit">Upload</button>
                </form>
                <h2>Available Files</h2>
                <ul>{file_links}</ul>
                <div class="footer">Simple File Server by Python</div>
            </div>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def handle_upload(self):
        content_length = int(self.headers['Content-Length'])
        boundary = self.headers['Content-Type'].split("=")[1].encode()
        line = self.rfile.readline()
        if boundary not in line:
            self.send_error(400, "Boundary not found")
            return

        filename_line = self.rfile.readline().decode()
        filename = filename_line.split('filename="')[1].split('"')[0]
        self.rfile.readline()  # empty line after content-disposition
        self.rfile.readline()  # content-type line

        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            while True:
                line = self.rfile.readline()
                if boundary in line:
                    break
                f.write(line)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

    def handle_download(self):
        query = parse_qs(urlparse(self.path).query)
        filename = query.get("file", [None])[0]
        if not filename or not os.path.exists(os.path.join(UPLOAD_DIR, filename)):
            self.send_error(404, "File not found")
            return

        file_path = os.path.join(UPLOAD_DIR, filename)
        self.send_response(200)
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Content-Length', os.path.getsize(file_path))
        self.send_header("Content-Type", "application/octet-stream")
        self.end_headers()

        with open(file_path, "rb") as f:
            self.wfile.write(f.read())

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8080)
    httpd = HTTPServer(server_address, FileServerHandler)
    print("Serving on port 8080...")
    httpd.serve_forever()
