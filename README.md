# Python EasyShare Server

Python EasyShare Server is a lightweight, web-based file server designed for easy file uploads and downloads. With a sleek, modern UI, it allows users to share files across devices on the same network using just a browser—no additional software required!

## Features

- **Simple Uploads and Downloads**: Upload files from one device and download them on another through a browser.
- **Responsive UI**: Clean, user-friendly design for easy navigation.
- **No Dependencies**: Built with Python’s standard libraries; no external packages required.

## Getting Started

### Prerequisites

- **Python 3.x**

### Installation

1. Clone the repository or download `file_server.py` directly.
   ```bash
   git clone https://github.com/InfoXMax/PythonLocalUploadHttpServer.git
   cd python-easyshare-server
   ```

2. Run the server:
   ```bash
   python3 file_server.py
   ```

3. Access the server:
   - Open a browser and go to `http://<YOUR_IP>:8080`.
   - You can now upload files and view/download them on any device connected to the same network.

## Usage

1. **Upload Files**: Select a file and click “Upload” to make it available on the server.
2. **Download Files**: Click on any uploaded file in the list to download it.

## Project Structure

- **file_server.py**: Main server script that handles file uploads and downloads.
- **uploads/**: Directory created to store uploaded files.

## Example

To use the server, run it in your terminal and open the given IP address in any browser. The interface will display an upload button and a list of available files.

## License

This project is open-source and available under the MIT License.

## Acknowledgments

Inspired by the need for a simple, stylish file-sharing solution using Python's standard library.
