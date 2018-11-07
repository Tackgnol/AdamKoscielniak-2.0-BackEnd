from mongoengine import *


class Project(EmbeddedDocument):
    Id = SequenceField()
    Title = StringField(max_length=120, required=True)
    Description = StringField(max_length=1000, required=True)
    Result = StringField(max_length=1000, required=True)
    PortfolioLink = URLField(max_length=200, required=False)
