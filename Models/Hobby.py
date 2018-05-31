from mongoengine import *

class Hobby(Document):
    Id = SequenceField()
    Name = StringField(max_length=120, required=True)
    Sort = IntField(required=True)
    Description = StringField(max_length=500, required=True)
    Photos = ListField(URLField(verify_exists=True))


