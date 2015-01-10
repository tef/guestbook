from datetime import datetime
from peewee import *

# Tell peewee what the database file is
# We use capital letters for this variable name according to custom, as it indicates
# something that will not change
DATABASE = "guestbook.db"
DATE = datetime.now().strftime("%H:%M - %d/%m/%y")
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

# We should only need to run the create_tables function once (and therefore,
# this database.py script once), each time a new model is created
# If a new field is added to the model, drop and recreate the table
def create_tables():
    database.connect()
    database.create_tables([Post])
    database.close()

# create_tables()

database.connect()

# Add a post to the database
post_one = Post.create(name="Jamiroquai", website="http://www.jamiroquai.co.uk", \
comment="Charlotte this guestbook is off the chain! You are 2kool4skool. Love Jam.", \
date=DATE)

post_two = Post.create(name="Satan", comment="666lol", date=DATE)

# Close the database
database.close()

print("Created a table!")
