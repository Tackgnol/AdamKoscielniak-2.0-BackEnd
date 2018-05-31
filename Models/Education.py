from mongoengine import *
from .SubModels.Project import Project
class Education(Document):
    Id = SequenceField()
    School = StringField(max_length=120, required=True)
    Level = StringField(max_length=120, required=True)
    Faculty = StringField(max_length=120, required=True)
    GradeEu = FloatField(min_value=2,max_value=5)
    GradeUs = StringField(max_length=5)
    BeginDate = DateTimeField(required=True)
    EndDate = DateTimeField(required=True)
    Projects = ListField(EmbeddedDocumentField(Project), required=False)
    Photos = ListField(URLField(verify_exists=True))

