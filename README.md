<img src="/assets/img/Python_3_blue.png" width="66" height="18">
<p align="center">
<img src="/assets/img/book.png" style="width: 60%;
max-width: 30em;">
</p>

## What is a "Guestbook"?

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

In this project; the script `guestbook.py` fetches the guestbook posts within the database, and displays them within the `index.html` template. I have not written
the HTML for each individual post within the index template, the script does that
for me. The cgi server within `server.py` allows me to do this on the website itself,
each time someone visits the guestbook the cgi script is activated and the posts
are displayed.

In 2015 we have server-side languages like [Ruby](https://www.ruby-lang.org/en/) and [Python](https://www.python.org), as well as client-side languages like [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) that can do this for us with ease without using cgi. This project is just a little homage to what
the web was only a decade or so ago.

<p align="center">
    <img src="/assets/img/hr.png">
</p>

## How can I use this guestbook?
**NB: These instructions only cover running the guestbook locally.
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

You can check to make sure the requirements are installed by running:

`pip freeze`

This should display peewee as the only package installed.

### Step Four: Run the guestbook!
Check out `guestbook.py` within the `cgi-bin` folder.
The only thing you need to do is make sure the first line is correct. Currently it
reads `#!/usr/bin/env python3`. This statement needs to be at the top of guestbook.py
so cgi knows what python version it is using.

Know that `guestbook.py` must live within the cgi-bin folder or else it won't work!

Now, we're ready to run our guestbook!

In your terminal, type: `python3 -m http.server --cgi`

Navigate to `http://localhost:8000/cgi-bin/guestbook.py` and you should see the guestbook in all it's glory! It should look something like [this](/assets/img/final.png)

---

## With thanks to:
- [@tef](https://twitter.com/tef) for the idea to go "Web 1.0" and use cgi in the first place as well as helping me debug
- [@jennschiffer](https://twitter.com/jennschiffer) for creating [make8bitart.com](http://make8bitart.com) so I could make sick graphics
- [Lissa Explains](http://lissaexplains.com) for still serving as inspiration, after all these years.
- [@pkqk](https://www.twitter.com/pkqk) and [@tom](https://twitter.com/tomwhoscontrary) for being patient and helpful

---

## Changelog:
- 13/01/2014: Guestbook released
- 15/01/2014: Minor updates: Merged #14 and made all code PEP8 compliant
