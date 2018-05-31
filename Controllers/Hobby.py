from main import app
from Models.Hobby import Hobby
from GlobalAPi.Result import Result
from flask import request
import json
import mongoengine
from mongoengine.errors import InvalidQueryError

@app.route('/hobby/add', methods=['POST'])
def AddHobby():
    result = Result()
    hobby = request.get_json(force = True)
    hobbyJSON = json.dumps(hobby) 
    try:
        job = Hobby.from_json(hobbyJSON)
        job.save()
        result.Value = hobby
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except mongoengine.errors.FieldDoesNotExist as e: 
        result.AddError(str(e))
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()

@app.route('/hobby/<id>', methods=['GET'])
def GetHobbyById(id):
    result = Result()
    try:
        hobby = Hobby.objects(Id=id)
        result.Value = hobby.first().to_json()
    except AttributeError:
        result.AddError('Hobby not found')
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()
    
@app.route('/hobby/<id>', methods=['PUT'])
def UpdateHobbyById(id):
    result = Result()
    update = request.get_json(force = True)
    try:
        dbObj = Hobby.objects.filter(Id = id).first()
        updateDbObj = dbObj.to_mongo()
        for (key,value) in update.items():
            updateDbObj[key] = value
        
        del updateDbObj['_id']
        dbObj.update(**updateDbObj)
        result.Value = json.dumps(updateDbObj)
    except AttributeError:
        result.AddError('This hobby does not exist, perhaps you wished to add it?')
    except InvalidQueryError: 
        result.AddError('Invalid field in the update statement, please review')
    except:
        result.AddError('Unknown error consult the system administrator')  
    return result.ToResponse()
@app.route('/hobby/<id>', methods=['DELETE'])
def DeleteHobbyById(id):
    result = Result()
    try: 
        toDelete = Hobby.objects.filter(Id = id).first()
        toDelete.delete()
        result.Value = "Element Removed succesfully"
    except AttributeError:
        result.AddError('This hobby does not exist, perhaps it was already deleted?')
    return result.ToResponse()

