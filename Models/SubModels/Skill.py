from mongoengine import *

class Skill(EmbeddedDocument):
    Id = SequenceField()
    Name = StringField(max_length=120, required=True)
    Experience = StringField(max_length=20, required=True)
    Sort = IntField(required=True)


