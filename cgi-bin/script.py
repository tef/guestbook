#!/Users/charlottespencer/.virtualenvs/guestbook/bin/python

import cgi
import cgitb; cgitb.enable()
# `re` allows us to work with regular expressions
import re

from peewee import *
from datetime import datetime


# Tell peewee what the database file is
# We use capital letters for this variable name according to custom, as it indicates
# something that will not change
DATABASE = "guestbook.db"
# Tell peewee to create a sqllite datbase called guestbook.db
database = SqliteDatabase(DATABASE)

# All models will inherit from this BaseModel, it saves us defined the database
# to use every time we create a new model
class BaseModel(Model):
    class Meta:
        database = database

# This is the model that lists all the information the guestbook form will collect
class Post(BaseModel):
    name = CharField()
    email = CharField(null=True)
    website = CharField(null=True)
    comment = TextField()
    date = DateTimeField()

template_file = "index.html"
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

def guestbook():
    guestbook_post = ""
    for post in Post.select().limit(10):
        guestbook_post += """<div class='post'>
                                <div class='comment'>
                                    <p class='text'>
                                        {0}
                                    </p>
                                    <p class='date'>
                                        {1}
                                    </p>
                                </div>

                                <div class="details">
                                    <span class='name'>{2}</span>
                          """.format(post.comment, post.date, post.name)
        if post.email:
            guestbook_post += """<span class='email'>
                                    | <a href='mailto:{0}'>@</a>
                                </span>
                              """.format(post.email)

        if post.website:
            guestbook_post += """<span class='website'>
                                    | <a href='{0}'>WWW</a>
                                 </span>
                              """.format(post.website)

        guestbook_post += """</div>
                             </div>

                             <hr>
                          """
    def visitor_counter():
        counter = open("counter.txt", "r")
        line = counter.readline()
        counter.close()

        if line == "":
            number = 1
        else:
            number = int(line) + 1

        counter = open("counter.txt", "w")
        counter.write(str(number))
        counter.close()

        visits = """
        <div id="counter">
            <p id="count">{0} visitors</p>
        </div>
        """.format(number)

        return visits

    return guestbook_post + visitor_counter()

def create_post():
    try:
        comment = form["comment"].value
    except:
        comment = "I didn't enter a comment :("

    try:
        name = form["name"].value
    except:
        print("Content-type: text/html")
        print()
        print("You need to at least submit a name. Please go back and try again!")
        raise SystemExit

    try:
        email = form["email"].value
    except:
        email = None

    try:
        website = form["website"].value
    except:
        website = None

    post = Post.create(
        comment=comment,
        name=form["name"].value,
        email=email,
        website=website,
        date=datetime.now().strftime("%H:%M - %d/%m/%y")
    )

# When we've submitted the form, this method will collect all the form data
form = cgi.FieldStorage()

try:
    key = form["key"].value
except:
    key = None


if key == "process":
    create_post()

# Display the guestbook!
display(guestbook())
