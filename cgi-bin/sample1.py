#!/usr/local/bin/python3

import cgi
# cgitb allows us to display errors with cgi in the browser
import cgitb; cgitb.enable()
# `re` allows us to work with regular expressions
import re

template_file = "template.html"
form_file = "form.html"

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

def display_form(form):
    # Open the form.html template in read only mode
    form_handle = open(form_file, "r")
    # Read the entire file as a string
    form_input = form_handle.read()
    # Close the form.html template
    form_handle.close()

    display(form_input)

def process_form(form):
    # Extract the information from the submitted form
    try:
        name = form["name"].value
    except:
        # name is required, so output an error if it is not given
        display("You need to at least supply a name!")
        raise SystemExit
    try:
        email = form["email"].value
    except:
        # If email doesn't exist, set it to None as it is optional
        email = None
    try:
        color = form["color"].value
    except:
        color = None
    try:
        comment = form["comment"].value
    except:
        comment = None

    output = ""
    output = output + "Hello,"

    if email != None:
        output = output + '<a href="mailto:{0}">{1}</a>'.format(email, name)
    else:
        output = output + name

    if color == "swallow":
        output = output + "You must be a Monty Python fan."
    elif color != None:
        output = output + "Your favourite color was {0}".format(color)
    else:
        output = output + "You cheated! You didn't specify a color!"

    if comment != None:
        output = output + "In addition, you said: <br> {0}".format(comment)

    display(output)

# Get form fields and their values
form = cgi.FieldStorage()

# key is a hidden form element with an action command like "process"
try:
    key = form["key"].value
except:
    key = None

if key == "process":
    process_form(form)
else:
    display_form()
