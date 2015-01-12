# Peewee allows us to worth with the database
from peewee import *
# Import datetime to use nicely formatted dates in our database
from datetime import datetime

# Tell peewee what the database file is
DATABASE = "guestbook.db"
# The dates will look like: 20:52 - 28/04/1991
DATE = datetime.now().strftime("%H:%M - %d/%m/%y")
# Tell peewee to create a sqllite datbase called guestbook.db
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

# We should only need to run the create_tables function once (and therefore,
# this database.py script once), each time a new model is created
# If a new field is added to the model, drop and recreate the table
def create_tables():
    database.connect()
    database.create_tables([Post])
    database.close()

# create_tables()

# Connect to the database to work with it
database.connect()

# Add some dummy posts to the database, feel free to change or delete this code
post_one = Post.create(name="Charlotte", website="http://charlotteis.github.io", \
comment="Thanks for installing my Guestbook!", \
date=DATE)

post_two = Post.create(name="Charlotte", website="http://twitter.com/charlotteis", \
comment="Check out the code on GitHub, where you'll also find guides on how to use this.", \
date=DATE)

post_one = Post.create(name="GitHub", website="http://www.github.com/charlotteis/guestbook", \
comment="Click on my WWW to see the code!", \
date=DATE)

# Close the database
database.close()

print("Created the database!")
