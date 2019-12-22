from mongoengine import *

class Address(EmbeddedDocument):
    StreetName = StringField(max_length=120, required=True)
    StreenNo = StringField(max_length=20, required=True)
    HouseNo = StringField(max_length=20)
    City = StringField(max_length=100, required=True)
    Country = StringField(max_length=100, required=True)

