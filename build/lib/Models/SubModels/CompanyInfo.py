import mongoengine
from Models.SubModels.Address import Address
class Company(mongoengine.EmbeddedDocument):
    Name = mongoengine.StringField(max_length=120, required=True)
    Website = mongoengine.URLField()    
    Business = mongoengine.StringField(max_length=100)
    Address= mongoengine.EmbeddedDocumentField(Address)

