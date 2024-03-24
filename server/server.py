import time
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from predict_result import get_emotion_predictions_from_base64_image;

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(bytes('ok', "utf8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        jsonBody = json.loads(post_body)
        base64String = jsonBody['base64']
        label, percentage = get_emotion_predictions_from_base64_image(base64String)
        data = {}
        data['label'] = label
        data['percentage'] = percentage
        response = json.dumps(data)
        self.wfile.write(bytes(response, "utf8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")