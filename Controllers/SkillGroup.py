from main import app
from Models.SkillGroup import SkillGroup
from GlobalAPi.Result import Result
from flask import request
import json
import mongoengine
from mongoengine.errors import InvalidQueryError
from flask_jwt_extended import jwt_required

import sys


@app.route('/skill/add', methods=['POST'])
@jwt_required
def AddSkillGroup():
    result = Result()
    skill = request.get_json(force=True)
    skillJSON = json.dumps(skill)
    try:
        job = SkillGroup.from_json(skillJSON)
        job.save()
        result.Value = skill
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except:
        print(sys.exc_info()[0])
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()


@app.route('/skill', methods=['GET'])
def GetSkills():
    result = Result()
    try:
        skills = SkillGroup.objects()
        result.Value = skills.to_json()
    except AttributeError:
        result.AddError('SkillGroup not found')
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()


@app.route('/skill/<id>', methods=['GET'])
def GetSkillGroupById(id):
    result = Result()
    try:
        skill = SkillGroup.objects(Id=id)
        result.Value = skill.first().to_json()
    except AttributeError:
        result.AddError('SkillGroup not found')
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()


@app.route('/skill/<id>', methods=['PUT'])
@jwt_required
def UpdateSkillGroupById(id):
    result = Result()
    update = request.get_json(force=True)
    try:
        dbObj = SkillGroup.objects.filter(Id=id).first()
        updateDbObj = dbObj.to_mongo()
        for (key, value) in update.items():
            updateDbObj[key] = value

        del updateDbObj['_id']
        dbObj.update(**updateDbObj)
        result.Value = dbObj.to_json()
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except AttributeError:
        result.AddError(
            'This skill does not exist, perhaps you wished to add it?')
    except InvalidQueryError:
        result.AddError('Invalid field in the update statement, please review')
    except:
        result.AddError('Unknown error consult the system administrator')
    return result.ToResponse()


@app.route('/skill/<id>', methods=['DELETE'])
@jwt_required
def DeleteSkillGroupById(id):
    result = Result()
    try:
        toDelete = SkillGroup.objects.filter(Id=id).first()
        toDelete.delete()
        result.Value = json.dumps(
            {'id': id, 'message': 'Succesfully removed element' + id})
    except AttributeError:
        result.AddError(
            'This skill does not exist, perhaps it was already deleted?')
    return result.ToResponse()


def SkillCount():
    totalSkills = 0
    groups = SkillGroup.objects()
    for skill in groups:
        totalSkills = totalSkills + len(skill.Skills)
    return totalSkills
