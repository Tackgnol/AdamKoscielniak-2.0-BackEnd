from main import app
from Models.Education import Education
from GlobalAPi.Result import Result
from flask import request
import json
import sys
import mongoengine
from mongoengine.errors import InvalidQueryError
from datetime import datetime
from flask_jwt_extended import jwt_required


@app.route('/education/add', methods=['POST'])
@jwt_required
def AddEducation():
    result = Result()
    education = request.get_json(force=True)
    educationJSON = json.dumps(education)
    try:
        job = Education.from_json(educationJSON)
        job.save()
        result.Value = education
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()


@app.route('/education', methods=['GET'])
def GetEducation():
    result = Result()
    expFrom = request.args.get('from') if request.args.get(
        'from') is not None else '1988-01-01'
    expTo = request.args.get('to') if request.args.get(
        'to') is not None else '3000-01-01'
    try:
        parsedDateFrom = datetime.strptime(expFrom, '%Y-%m-%d')
        parsedDateTo = datetime.strptime(expTo, '%Y-%m-%d')

    except ValueError:
        result.AddError('Invalid Datetime format')

    if parsedDateFrom > parsedDateTo:
        result.AddError('Date from cannot be greater then Date from')
        return result.ToResponse()

    query_education = Education.objects(
        BeginDate__gte=parsedDateFrom, EndDate__lte=parsedDateTo)

    result.Value = query_education.to_json()
    return result.ToResponse()


@app.route('/education/<id>', methods=['GET'])
def GetEducationById(id):
    result = Result()
    try:
        education = Education.objects(Id=id)
        result.Value = education.first().to_json()
    except AttributeError:
        result.AddError('Education not found')
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()


@app.route('/education/<id>', methods=['PUT'])
@jwt_required
def UpdateEducationById(id):
    result = Result()
    update = request.get_json(force=True)
    try:
        dbObj = Education.objects.filter(Id=id).first()
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
            'This education does not exist, perhaps you wished to add it?')
    except InvalidQueryError:
        result.AddError('Invalid field in the update statement, please review')
    except:
        result.AddError(sys.exc_info()[0])
    return result.ToResponse()


@app.route('/education/<id>', methods=['DELETE'])
@jwt_required
def DeleteEducationById(id):
    result = Result()
    try:
        toDelete = Education.objects.filter(Id=id).first()
        toDelete.delete()
        result.Value = json.dumps(
            {'id': id, 'message': 'Succesfully removed element' + id})
    except AttributeError:
        result.AddError(
            'This education does not exist, perhaps it was already deleted?')
    return result.ToResponse()
