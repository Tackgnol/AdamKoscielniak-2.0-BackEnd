from mongoengine import *

class Project(EmbeddedDocument):
    Title = StringField(max_length=120, required=True)
    Description = StringField(max_length=120, required=True)
    Result = StringField(max_length=120, required=True)
    PortfolioLink = URLField(max_length=200, required=False)

