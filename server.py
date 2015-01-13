import http.server

PORT = 8000
HOST = "127.0.0.1"

# This will display the site at `http://localhost:8000/`
server_address = (HOST, PORT)

# The CGIHTTPRequestHandler class allows us to run the cgi script in /cgi-bin/
# Rather than attempt to display the cgi file itself, which a 'BaseHTTPRequestHandler' or
# 'SimpleHTTPRequestHandler' may do
httpd = http.server.HTTPServer(server_address, http.server.CGIHTTPRequestHandler)
print("Starting my web server on port {0}".format(PORT))
# Make sure the server is always serving the content
# You can stop the server running using CTRL + C
httpd.serve_forever()
