from mongoengine import *


class Skill(EmbeddedDocument):
    Id = SequenceField()
    Name = StringField(max_length=120, required=True)
    Proficiency = DecimalField(
        min_value=0, max_value=1, force_string=False, precision=2, rounding='ROUND_HALF_UP')
    Sort = IntField()
