from mongoengine import *


class Social(Document):
    Name = StringField(max_length=120, required=True)
    Sort = IntField()
    Url = StringField(max_length=500, required=True)
    FAIcon = StringField(max_length=50, required=True)

