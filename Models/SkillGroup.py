from mongoengine import *
from .SubModels.Skill import Skill
class SkillGroup(Document):
    Id = SequenceField()
    Name = StringField(max_length=120, required=True)
    Sort = IntField(required=True)
    Skills = ListField(EmbeddedDocumentField(Skill), required=True)


