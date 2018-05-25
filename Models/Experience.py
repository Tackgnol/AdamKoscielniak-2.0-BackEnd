from mongoengine import *
from . import Project
class Experience(Document):
    Id = SequenceField()
    Employer = StringField(max_length=120, required=True)
    Position = StringField(max_length=120, required=True)
    Responsibilities = ListField(StringField(max_length=500), required=True)
    CurrentEmployer = BooleanField(default=False)
    BeginDate = DateTimeField(required=True)
    EndDate = DateTimeField(required=True)
    Projects = ListField(EmbeddedDocumentField(Project.Project), required=False)



