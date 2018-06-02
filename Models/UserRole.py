from mongoengine import *

class UserRole(Document):
    Name = StringField(max_length=100)
    IsAdmin = BooleanField(default=False)

