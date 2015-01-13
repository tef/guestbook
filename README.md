<img src="/assets/img/Python_3_blue.png" width="66" height="18">
<p align="center">
<img src="/assets/img/book.png" style="width: 60%;
max-width: 30em;">
</p>

## What is "Guestbook"?

When I first started using the Internet, guestbooks were popular.
I'd be able to go to a website like [Lissa Explains](http://www.lissaexplains.com/guestbook.shtml)
(which serves as the inspiration for this project) and leave a message with my name and a
comment to the author of the website. It was a way of messaging people before you had
your Facebooks and your Twitters.

For me, it was my first understanding that people
all over the world could converge at the same place at the same time, to talk to each other.

## What is "cgi"?
Common Gateway Interface (CGI) was what these original guestbooks were powered on.
CGI was [introduced in 1993](http://en.wikipedia.org/wiki/Common_Gateway_Interface#History) and kickstarted
the move from websites just displaying static HTML (unmodified by scripts) to being
able to run scripts on your web server and displaying the results on your website.

In this project; the script `script.py` fetches the guestbook posts within the database, and displays them within the `index.html` template. I have not written
the HTML for each individual post within the index template, the script does that
for me. The cgi server within `server.py` allows me to do this on the website itself,
each time someone visits the guestbook the cgi script is activated and the posts
are displayed.

In 2015 we have server-side languages like [Ruby](https://www.ruby-lang.org/en/) and [Python](https://www.python.org), as well as client-side languages like [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) that can do this for us with ease. In fact, the cgi technology used in this project is powered by a cgi module within the Python language. This project is just a little homage to what
the web was only a decade or so ago.

## How can I use this guestbook?
**NB: So far these instructions will only cover running the guestbook locally.
I'd like to write instructions on running this project on a free application hosting service like [Heroku](https://www.heroku.com). [Help with this is appreciated](https://github.com/Charlotteis/guestbook/issues/1)**.

### Step One: Grab the code!
You can do this either by cloning the repository if you're familiar with the command line

`git clone https://github.com/Charlotteis/guestbook.git`

OR by cloning it within the graphical GitHub client for [Windows](https://windows.github.com)
or [Mac](https://mac.github.com)

OR by downloading the [.zip file](https://github.com/Charlotteis/guestbook/archive/master.zip) directly

### Step Two: Install the required packages!
I recommend working within a [virtual environment](https://virtualenv.pypa.io/en/latest/)
when you work with this code, because it keeps all your dependencies nice and tidy
and things are less likely to break.

Check the `requirements.txt` file for the required dependencies.
The only one we are using for this application is [peewee](https://peewee.readthedocs.org/en/latest/)
which helps to manage our guestbook database. To install peewee you will need to have [pip]
(https://pypi.python.org/pypi/pip) already installed.

Within your virtual environment run the following command:

`pip install -r requirements.txt`

### Step Three: Create your database!

First, check out the `database.py` file. This is what we will run to create our database.
The line: `DATABASE = "guestbook.db"` sets the name of your database. If you want
it to be called something else, change `"guestbook.db"` to "`whateveryouwant.db`"

Second, check out the dummy posts that will be created when you run this file.
Unless you change it, it will create some default posts in my name. Feel free to change the details
or delete these dummy posts altogether!

Thirdly, uncomment the single line of code `create_tables()`. This will make sure
that a database is created for you with your chosen name so you can work with the guestbook.

Lastly, run the following in your terminal (within the virtual env and project directory):

`python3 database.py`

If you see `"Created the database!"` then you have successfully created your database!
You can now comment out `create_tables()`. If you want to re-create your database
you can delete the database file, uncomment `create_tables()` and run `python3 database.py` again.

### Step Four: Run the guestbook!
Firstly, check out the `server.py` file. It's a small file that will allow you to run
the files within this project locally on your machine.

I've made it so the project files will run on localhost:8000. Feel free to change the `PORT`
within the server file.

Now, check out `script.py` within the `cgi-bin` folder.
The only thing you need to do is make sure the first line is correct. Currently it
reads `#!/usr/bin/python3`. This statement needs to be at the top of script.py
so cgi knows what python version it is using. The guestbook _may_ work with this line how it is.
But all our machines are likely different so you need to check. This may be simply done by running
`which python3` within your terminal. Copy the output and put it at the top of `script.py` with the `#!` at the start.

Know that `script.py` must live within the cgi-bin folder or else it won't work!

Now, we're ready to run our guestbook!

In your terminal, type: `python3 server.py`

Navigate to `http://localhost:8000/cgi-bin/script.py` and you should see the guestbook
in all it's glory! It should look something like [this](/assets/img/final.png)

---

## With thanks to:
- [@tef](https://twitter.com/tef) for the idea to go "Web 1.0" and use cgi in the first place
- [@jennschiffer](https://twitter.com/jennschiffer) for creating [make8bitart.com](http://make8bitart.com) so I could make sick graphics
- [Lissa Explains](http://lissaexplains.com) for still serving as inspiration, after all these years.

---

## Changelog:
