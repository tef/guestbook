#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()

print("Content-type: text/html")
print()
print("<html><body>")
for i in range(0, 15):
    print(i, "<br>")
print("</body></html>")
