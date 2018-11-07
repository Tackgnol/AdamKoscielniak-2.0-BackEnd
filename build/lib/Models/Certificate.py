from mongoengine import *

class Certificate(Document):
    Id = SequenceField()
    SkillGroup = StringField(max_length=120, required=True)
    Name = StringField(max_length=120, required=True)
    Teacher = StringField(max_length=120, required=True)
    TeacherWebsite = URLField()
    Organizer = StringField(max_length=120, required=True)
    OrganizerWebsite = URLField()
    BeginDate = DateTimeField(required=True)
    EndDate = DateTimeField(required=True)
    Scans = ListField(URLField(verify_exists=True))


