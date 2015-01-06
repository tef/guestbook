#!/usr/local/bin/python3

import cgi
import cgitb; cgitb.enable()

# Tell the browser how to render the text
print("Content-type: text/html")
print()

# Get all the form inputs, which will give a dictionary of tuples
# EG: {"name": ("name", "value")}
Form = cgi.FieldStorage()

# Print the name of each input and it's associated value
for name in Form.keys():
    print("Input: {0}, Value: {1}".format(name, Form[name].value))
    print("<br>")

print("<html><body>")
print("Finished!")
print("</body></html>")
