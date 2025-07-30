
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

host = "localhost"
port = 8000

# Helper function to check for Spring4Shell patterns
def is_malicious_request(path, method, headers, body):
    # Check if path is the malicious JSP endpoint
    if path != "/tomcatwar.jsp":
        return False

    # Check if it's a POST request
    if method != "POST":
        return False

    # Check malicious headers
    if headers.get("suffix") == "%>//" and headers.get("c1") == "Runtime" and headers.get("c2") == "<%" and        headers.get("Content-Type") == "application/x-www-form-urlencoded" and headers.get("DNT") == "1":
        return True

    # Check body content
    if "class.module.classLoader" in body:
        return True

    return False

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.allow_request()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        if is_malicious_request(self.path, "POST", self.headers, body):
            self.block_request()
        else:
            self.allow_request()

    def allow_request(self):
        print("✅ Allowed request")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "allowed"}')

    def block_request(self):
        print("❌ Blocked malicious request")
        self.send_response(403)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "blocked"}')

if __name__ == "__main__":
    server = HTTPServer((host, port), ServerHandler)
    print("[+] Firewall Server running on: %s:%s" % (host, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("[+] Server terminated. Exiting...")
    exit(0)
