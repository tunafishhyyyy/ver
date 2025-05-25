import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs

        print("[INFO] Received GET request: ", self.path)

        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', [])
        print(f"[DEBUG] Parsed query parameters: {query}")
        print(f"[DEBUG] Names extracted: {names}")

        # Load and convert the JSON array to a dictionary for fast lookup
        json_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
        print(f"[INFO] Loading JSON data from: {json_path}")
        try:
            with open(json_path) as f:
                data_list = json.load(f)
                print(f"[DEBUG] Loaded data list: {data_list}")
                data = {item["name"]: item["marks"] for item in data_list}
                print(f"[DEBUG] Converted data to dict: {data}")
        except Exception as e:
            print(f"[ERROR] Failed to load or parse JSON file: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Internal Server Error"}).encode())
            return

        # For each requested name, get the mark or None (which becomes null in JSON)
        marks = [data.get(name, None) for name in names]
        print(f"[INFO] Marks to return: {marks}")

        # Respond with the required JSON
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"marks": marks}
        print(f"[INFO] Sending response: {response}")
        self.wfile.write(json.dumps(response).encode())
