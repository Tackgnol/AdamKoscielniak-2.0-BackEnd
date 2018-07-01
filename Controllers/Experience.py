from main import app
from Models.Experience import Experience
from GlobalAPi.Result import Result
from flask import request, Response
import json
from datetime import datetime
import mongoengine
from mongoengine.errors import InvalidQueryError


@app.route('/experience/add', methods=['POST'])
def AddExperience():
    result = Result()
    experience = request.get_json(force=True)
    experienceJSON = json.dumps(experience)
    try:
        job = Experience.from_json(experienceJSON)
        job.save()
        result.Value = experience
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()


@app.route('/experience/<id>', methods=['GET'])
def GetExperienceById(id):
    result = Result()
    try:
        experience = Experience.objects(Id=id)
        result.Value = experience.first().to_json()
    except AttributeError:
        result.AddError('Experience not found')
    except Exception:
        result.AddError('Unknown error consult the system administrator')

    resp = Response(result.ToResponse())
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


@app.route('/experience/<id>', methods=['PUT'])
def UpdateExperienceById(id):
    result = Result()
    update = request.get_json(force=True)
    try:
        dbObj = Experience.objects.filter(Id=id).first()
        updateDbObj = dbObj.to_mongo()
        for (key, value) in update.items():
            updateDbObj[key] = value

        del updateDbObj['_id']
        dbObj.update(**updateDbObj)
        result.Value = dbObj.to_json()
    except AttributeError:
        result.AddError(
            'This experience does not exist, perhaps you wished to add it?')
    except InvalidQueryError:
        result.AddError('Invalid field in the update statement, please review')
    except Exception:
        result.AddError('Unknown error consult the system administrator')
    return result.ToResponse()


@app.route('/experience', methods=['GET'])
def GetExperiences():
    result = Result()
    expFrom = request.args.get('from') if request.args.get(
        'from') is not None else '1988-01-01'
    expTo = request.args.get('to') if request.args.get(
        'to') is not None else '3000-01-01'
    expSkills = request.args.get('skills').split(',') if request.args.get(
        'skills') is not None else []

    try:
        parsedDateFrom = datetime.strptime(expFrom, '%Y-%m-%d')
        parsedDateTo = datetime.strptime(expTo, '%Y-%m-%d')

    except ValueError:
        result.AddError('Invalid Datetime format')

    if parsedDateFrom > parsedDateTo:
        result.AddError('Date from cannot be greater then Date from')
        return result.ToResponse()

    query_experience = Experience.objects(
        BeginDate__gte=parsedDateFrom, EndDate__lte=parsedDateTo)

    if len(expSkills) > 0:
        query_experience = query_experience.filter(Skills__all=expSkills)

    result.Value = query_experience.to_json()

    return result.ToResponse()


@app.route('/experience/<id>', methods=['DELETE'])
def DeleteExperieceById(id):
    result = Result()
    try:
        toDelete = Experience.objects.filter(Id=id).first()
        toDelete.delete()
        result.Value = "Element Removed succesfully"
    except AttributeError:
        result.AddError(
            'This experience does not exist, perhaps it was already deleted?')
    return result.ToResponse()
