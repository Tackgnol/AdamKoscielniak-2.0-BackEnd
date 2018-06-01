from mongoengine import *
from Models.SubModels.Address import Address
class Company(EmbeddedDocument):
    Name = StringField(max_length=120, required=True)
    Website = URLField()    
    Business = StringField(max_length=100)
    Address= EmbeddedDocumentField(Address)

