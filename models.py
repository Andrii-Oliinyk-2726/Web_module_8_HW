import certifi
from mongoengine import *

uri = "mongodb+srv://oland2726:llRPcLo2d4iN4Ay0@cluster0.chqoczf.mongodb.net/web_hw_8?retryWrites=true&w=majority"
connection = connect(host=uri,  tlsCAFile=certifi.where(), ssl=True)


class Author(Document):

    fullname = StringField(max_length=50)
    born_date = StringField(max_length=50)
    # born_date = DateTimeField()
    born_location = StringField(max_length=50)
    description = StringField()


class Quote(Document):

    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    quote = StringField(max_length=1200, required=True)

    meta = {'allow_inheritance': True}


class TextPost(Quote):
    content = StringField()
