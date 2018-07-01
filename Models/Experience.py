from mongoengine import *
from .SubModels.Project import Project


class Experience(Document):
    Id = SequenceField()
    Employer = StringField(max_length=120, required=True)
    Position = StringField(max_length=120, required=True)
    Responsibilities = ListField(StringField(max_length=500), required=True)
    Skills = ListField(StringField(max_length=100))
    CurrentEmployer = BooleanField(default=False)
    BeginDate = DateTimeField(required=True)
    EndDate = DateTimeField(required=True)
    Projects = ListField(EmbeddedDocumentField(Project), required=False)
    Photos = ListField(URLField(verify_exists=True))
