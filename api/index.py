import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs

        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', [])

        # Load and convert the JSON array to a dictionary for fast lookup
        json_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
        with open(json_path) as f:
            data_list = json.load(f)
            data = {item["name"]: item["marks"] for item in data_list}

        # For each requested name, get the mark or None (which becomes null in JSON)
        marks = [data.get(name, None) for name in names]

        # Respond with the required JSON
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"marks": marks}).encode())
