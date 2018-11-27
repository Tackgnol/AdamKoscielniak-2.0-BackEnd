from main import app, jwt
from Models.Experience import Experience
from GlobalAPi.Result import Result
from flask import request, Response
import json
from datetime import datetime, timedelta
import mongoengine
import sys
from mongoengine.errors import InvalidQueryError
from flask_jwt_extended import jwt_required
from mongoengine.queryset.visitor import Q


@app.route('/experience/add', methods=['POST'])
@jwt_required
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


@app.route('/experience/current', methods=['GET'])
def GetCurrentExperience():
    result = Result()
    try:
        experience = Experience.objects().first()
        experience.Projects = None
        result.Value = experience.to_json()
    except AttributeError:
        result.AddError('Experience not found')
    except Exception:
        result.AddError('Unknown error consult the system administrator')

    resp = Response(result.ToResponse())
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


@app.route('/experience/<id>', methods=['POST'])
@jwt_required
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
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except AttributeError:
        result.AddError(
            'This experience does not exist, perhaps you wished to add it?')
    except InvalidQueryError:
        result.AddError('Invalid field in the update statement, please review')
    except Exception:
        result.AddError(result.AddError(sys.exc_info()[0]))
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

        if(request.args.get('to') is None):
            toQueryObject = (Q(EndDate__gte=parsedDateFrom) | Q(EndDate=None))
        else:
            toQueryObject = Q(EndDate__gte=parsedDateFrom)
    except ValueError:
        result.AddError('Invalid Datetime format')

    if parsedDateFrom > parsedDateTo:
        result.AddError('Date from cannot be greater then Date from')
        return result.ToResponse()

    query_experience = Experience.objects(
        Q(BeginDate__lte=parsedDateTo) & toQueryObject)

    if len(expSkills) > 0:
        query_experience = query_experience.filter(Skills__all=expSkills)

    result.Value = query_experience.to_json()

    return result.ToResponse()


@app.route('/experience/<id>', methods=['DELETE'])
@jwt_required
def DeleteExperieceById(id):
    result = Result()
    try:
        toDelete = Experience.objects.filter(Id=id).first()
        toDelete.delete()
        result.Value = json.dumps(
            {'id': id, 'message': 'Succesfully removed element' + id})
    except AttributeError:
        result.AddError(
            'This experience does not exist, perhaps it was already deleted?')
    return result.ToResponse()


def TotalTimeWorked(expFrom, expTo, expSkills):

    parsedDateFrom = datetime.strptime(expFrom, '%Y-%m-%d').date()
    parsedDateTo = datetime.strptime(expTo, '%Y-%m-%d').date()
    if parsedDateFrom > parsedDateTo:
        return 0

    if(request.args.get('to') is None):
        toQueryObject = (Q(EndDate__gte=parsedDateFrom) | Q(EndDate=None))
    else:
        toQueryObject = Q(EndDate__gte=parsedDateFrom)

    query_experience = Experience.objects(
        Q(BeginDate__lte=parsedDateTo) & toQueryObject)

    if len(expSkills) > 0:
        query_experience = query_experience.filter(Skills__all=expSkills)
    totalHours = 0
    for experience in query_experience:
        start = experience.BeginDate
        end = experience.EndDate if experience.EndDate is not None else datetime.now()
        daygenerator = (start + timedelta(x + 1)
                        for x in range((end - start).days))
        days = sum(1 for day in daygenerator if day.weekday() < 5)
        totalHours = totalHours + days*8
    return totalHours


def TotalWorkProjects(expFrom, expTo, expSkills):
    parsedDateFrom = datetime.strptime(expFrom, '%Y-%m-%d').date()
    parsedDateTo = datetime.strptime(expTo, '%Y-%m-%d').date()

    if(request.args.get('to') is None):
        toQueryObject = (Q(EndDate__gte=parsedDateFrom) | Q(EndDate=None))
    else:
        toQueryObject = Q(EndDate__gte=parsedDateFrom)

    if parsedDateFrom > parsedDateTo:
        return 0

    query_experience = Experience.objects(
        Q(BeginDate__lte=parsedDateTo) & toQueryObject)

    if len(expSkills) > 0:
        query_experience = query_experience.filter(Skills__all=expSkills)
    totalProjects = 0
    for experience in query_experience:
        totalProjects = totalProjects + len((experience.Projects))
    return totalProjects
