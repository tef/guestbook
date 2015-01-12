#!/Users/charlottespencer/.virtualenvs/guestbook/bin/python

import cgi
# cgitb allows us to view cgi errors, best to comment it out when using in production
import cgitb; cgitb.enable()
# `re` allows us to work with regular expressions
import re

# Peewee allows us to work with the guestbook database
from peewee import *
from datetime import datetime


# Tell peewee what the database file is
DATABASE = "guestbook.db"
# Tell peewee it is working with a Sqlite database
database = SqliteDatabase(DATABASE)

# All models will inherit from this BaseModel, it saves us defining the database
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

# This is where we will insert our guestbook posts
template_file = "index.html"

def display(content):
    """ Displays HTML within the template file

        Subsitutes "<!--INSERT CONTENT HERE-->" within the index file
        content = the HTML you wish to display
    """

    # Open template file in read only mode
    template_handle = open(template_file, "r")
    # Read the entire file as a string
    template_input = template_handle.read()
    # Close the file
    template_handle.close()

    template_error = "There was a problem with the HTML template"

    # Replace "INSERT CONTENT HERE" with 'content'
    sub_result = re.subn("<!--INSERT CONTENT HERE-->", content, template_input)
    if sub_result[1] == 0:
        raise Exception(template_error)

    # Tell the page that it is HTML
    print("Content-type: text/html")
    # This blank line MUST be printed after the content-type statement
    print()
    # Print the substituted content
    print(sub_result[0])

def guestbook():
    """ Retrieves the posts from the database and converts them to HTML
    """

    guestbook_post = ""
    # limit(10) means that only the latest ten guestbook posts will be displayed
    # For each of the ten posts, conver them to HTML
    for post in Post.select().limit(10).order_by(Post.date.desc()):
        # Start the individual post HTML
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

        # If an email was submitted, add it to the post
        if post.email:
            guestbook_post += """<span class='email'>
                                    | <a href='mailto:{0}'>@</a>
                                </span>
                              """.format(post.email)

        # If a website was submitted, add it to the post
        if post.website:
            guestbook_post += """<span class='website'>
                                    | <a href='{0}'>WWW</a>
                                 </span>
                              """.format(post.website)

        # End the individual post HTML
        guestbook_post += """</div>
                             </div>

                             <hr>
                          """

    def visitor_counter():
        """ Displays the number of visitors to the website
            Currently executed each time the script is loaded (which is bad)
        """

        # The counter is stored in 'counter.txt', open the file for reading (r+)
        counter = open("counter.txt", "r")
        line = counter.readline()
        counter.close()

        # If 'counter.txt' is empty, add a count of one,
        # If a number already exists, add one to it
        if line == "":
            number = 1
        else:
            number = int(line) + 1

        # Open counter for writing
        counter = open("counter.txt", "w")
        # Add the counter to counter.txt
        counter.write(str(number))
        # Close the counter.txt file
        counter.close()

        # Add the counter to the index page
        visits = """
        <div id="counter">
            <p id="count">{0} visitors</p>
        </div>
        """.format(number)

        return visits

    # Return the guestbook posts HTML, followed by the visitor counter
    return guestbook_post + visitor_counter()

def create_post():
    """ Creates a post in the database depending on the form information submitted
    """

    # If no comment was submitted, set a default
    try:
        comment = form["comment"].value
    except:
        comment = "I didn't enter a comment :("

    # If no name was submitted exists, ask the person to try again and stop the script
    try:
        name = form["name"].value
    except:
        print("Content-type: text/html")
        print()
        print("You need to at least submit a name. Please go back and try again!")
        raise SystemExit

    # If no email submitted, set it as 'None' so it can be passed to the database
    try:
        email = form["email"].value
    except:
        email = None

    # If no website submitted, set it as 'None' so it can be passed to the database
    try:
        website = form["website"].value
    except:
        website = None

    # Create a post in the database using the form information!
    post = Post.create(
        comment=comment,
        name=form["name"].value,
        email=email,
        website=website,
        date=datetime.now().strftime("%H:%M - %d/%m/%y")
    )

# When we've submitted the form, this method will collect all the form data
form = cgi.FieldStorage()

# If the hidden key does not exist, set it to None which will prevent the script
# From creating the post
try:
    key = form["key"].value
except:
    key = None

# If the hidden key within the form is present, try to create a post
if key == "process":
    create_post()

# Display the guestbook!
display(guestbook())
