import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs

        print("[INFO] Received GET request: ", self.path)
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', [])
        print(f"[DEBUG] Parsed query parameters: {query}")

        json_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
        print(f"[INFO] Loading JSON data from: {json_path}")
        try:
            with open(json_path) as f:
                data_list = json.load(f)
                data = {item["name"]: item["marks"] for item in data_list}
        except Exception as e:
            print(f"[ERROR] Failed to load or parse JSON file: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # CORS header on error
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Internal Server Error"}).encode())
            return

        marks = [data.get(name, None) for name in names]
        print(f"[INFO] Marks to return: {marks}")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # <-- Enable CORS
        self.end_headers()
        self.wfile.write(json.dumps({"marks": marks}).encode())
