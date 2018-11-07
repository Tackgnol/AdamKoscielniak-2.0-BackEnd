from mongoengine import *


class Hobby(Document):
    Id = SequenceField()
    Name = StringField(max_length=120, required=True)
    Sort = IntField()
    Description = StringField(max_length=500, required=True)
    FAIcon = StringField(max_length=50, required=True)
    Photos = ListField(URLField(verify_exists=True))
