#!/usr/bin/env python3

import cgi
import cgitb
import re
import os
import urllib
from datetime import datetime

import peewee as pw

# cgitb allows us to view cgi errors, best to comment it out for in production
cgitb.enable()

template_file = "assets/html/index.html"
form_template_file = "assets/html/form.html"

DATABASE = os.environ.get("DATABASE_URL","guestbook.db")
if DATABASE.startswith("postgres"):
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(DATABASE)
    database = pw.PostgresqlDatabase(
        url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
else:
    database = pw.SqliteDatabase(DATABASE)

# All models will inherit from BaseModel, it saves us defining the database
# to use every time we create a new model
class BaseModel(pw.Model):
    class Meta:
        database = database


# This is the model that lists all the info the guestbook form will collect
class Post(BaseModel):
    name = pw.CharField()
    email = pw.CharField(null=True)
    website = pw.CharField(null=True)
    comment = pw.TextField()
    date = pw.DateTimeField()

class Visitor(BaseModel):
    count = pw.IntegerField(default=0)

database.create_tables([Post, Visitor], True)

def main():
    method = os.environ.get('REQUEST_METHOD', 'GET')
    query_string = os.environ.get('QUERY_STRING', '')
    script_name = os.environ.get('SCRIPT_NAME', '/cgi-bin/guestbook.py')

    if method == "POST":
        # When we've submitted the form, this method will collect all the form data
        form = cgi.FieldStorage()
        if create_post(form):
            # If successful, redirect to the view guestbook page
            print("Location: {}".format(script_name), end="\r\n")
            print("Refresh: 0;URL={}".format(script_name), end="\r\n") # Python cgi doesn't like sending redirects.
            print("", end="\r\n")
            print("Redirecting", end="\r\n")
        else:
            # Or show an error
            display("<h2>You need to at least submit a name. \
                  Please try again!</h2>", form_template_file)
    elif query_string == "sign":
        # Use a different template
        display("", form_template_file)
    else:
        # Display the guestbook!
        template_file = "assets/html/index.html"
        
        display(render_guestbook() + visitor_counter(), template_file)



def create_post(form):
    """ Creates a post in the database depending on the form information submitted
    """

    # If no comment was submitted, set a default
    try:
        comment = form["comment"].value
    except:
        comment = "I didn't enter a comment :("

    # If no name was submitted, ask the person to try again and stop the script
    try:
        name = form["name"].value
    except:
        return False

    # If no email, set it as 'None' so it can be passed to the database
    try:
        email = form["email"].value
    except:
        email = None

    # If no website, set it as 'None' so it can be passed to the database
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
        date=datetime.utcnow()
    )
    return True

def render_guestbook():
    """ Retrieves the posts from the database and converts them to HTML
    """

    guestbook_post = ""
    # limit(10) means that only the latest ten posts will be displayed
    # For each of the ten posts, conver them to HTML
    for post in Post.select().order_by(Post.date.desc()).limit(10):
        # Start the individual post HTML
        guestbook_post += """<article class='post' role="article">
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
                                    | <a href='mailto:{0}' tabindex="1">@</a>
                                </span>
                              """.format(post.email)

        # If website submitted and begins with "http://"
        # or "https://", add it to the post
        if post.website and (post.website.startswith("http://") or
                             post.website.startswith("https://")):
            guestbook_post += """<span class='website'>
                                    | <a href='{0}' tabindex="1">WWW</a>
                                 </span>
                              """.format(post.website)

        # Else if there is a website that doesn't start with "http://" or
        # https://, add "http://" to start of the URL and add URL to the post
        elif post.website:
            guestbook_post += """<span class='website'>
                                    | <a href='http://{0}' tabindex="1">WWW</a>
                                 </span>
                              """.format(post.website)

        # End the individual post HTML
        guestbook_post += """</div>
                             </article>

                             <hr>
                          """
    return guestbook_post

def visitor_counter():
    """ Displays the number of visitors to the website
        Currently executed each time the script is loaded (which is bad)
    """

    with database.atomic():
        visitors =  list(Visitor.select().limit(1))
        if not visitors:
            visitor = Visitor.create(count=1)
        else:
            visitor = visitors[0]

        visitor.count = visitor.count + 1
        visitor.save()

    number = visitor.count

    # Add the counter to the index page
    if number == 1:
        visits = """
        <div id="counter">
            <p id="count">{0} visitor</p>
        </div>
        """.format(number)
    else:
        visits = """
        <div id="counter">
            <p id="count">{0} visitors</p>
        </div>
        """.format(number)

    return visits

def display(content, template_file):
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
    if sub_result[1] == 0 and content:
        raise Exception(template_error)

    # Tell the page that it is HTML
    print("Content-type: text/html", end="\r\n")
    # This blank line MUST be printed after the content-type statement
    print(end="\r\n")
    # Print the substituted content
    print(sub_result[0], end="\r\n")

if __name__ == "__main__":
    main()

