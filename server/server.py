#!/usr/bin/python3.4

__author__ = "Jeremy Rabasco"

from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
hostPort = 31415


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>THIS WORKS !</h1>")


myServer = HTTPServer((hostName, hostPort), MyServer)

print("Server Starts :", hostName, "-", hostPort)

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print("Server Stops :", hostName, "-", hostPort)
