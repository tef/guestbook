#!/usr/local/bin/python3

import cgi
import cgitb; cgitb.enable()
# `re` allows us to work with regular expressions
import re

template_file = "template.html"

def display(content):
    # Open template file in read only mode
    template_handle = open(template_file, "r")
    # Read the entire file as a string
    template_input = template_handle.read()
    # Close the file
    template_handle.close()

    template_error = "There was a problem with the HTML template"

    sub_result = re.subn("<!--INSERT CONTENT HERE-->", content, template_input)
    if sub_result[1] == 0:
        raise Exception(template_error)

    print("Content-type: text/html")
    # This blank line MUST be printed after the content-type statement
    print()
    print(sub_result[0])

display("Hello?")

# # Tell the browser how to render the text
# print("Content-type: text/html")
# print()
#
# # Get all the form inputs, which will give a dictionary of tuples
# # EG: {"name": ("name", "value")}
# Form = cgi.FieldStorage()
#
# # Print the name of each input and it's associated value
# for name in Form.keys():
#     print("Input: {0}, Value: {1}".format(name, Form[name].value))
#     print("<br>")
#
# print("<html><body>")
# print("Finished!")
# print("</body></html>")
