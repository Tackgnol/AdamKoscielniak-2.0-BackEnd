from mongoengine import *

from Models.SubModels.CompanyInfo import Company

class User(Document):
    Id = SequenceField()
    FirstName = StringField(max_length=120)
    LastName = StringField(max_length=120)
    Email = EmailField(required=True, unique=True)
    Password = StringField(max_length=100, required=True)
    AccountType = StringField(max_length=20, required=True)
    Company = EmbeddedDocumentField(Company)

class TokenInfo:
        def __init__(self, username, roles):
            self.username = username
            self.role = roles
