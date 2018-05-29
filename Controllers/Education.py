from main import app
from Models.Education import Education
from GlobalAPi.Result import Result
from flask import request
import json
import mongoengine
from mongoengine.errors import InvalidQueryError

@app.route('/education/add', methods=['POST'])
def AddEducation():
    result = Result()
    education = request.get_json(force = True)
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
def UpdateEducationById(id):
    result = Result()
    update = request.get_json(force = True)
    try:
        dbObj = Education.objects.filter(Id = id).first()
        updateDbObj = dbObj.to_mongo()
        for (key,value) in update.items():
            updateDbObj[key] = value
        
        del updateDbObj['_id']
        dbObj.update(**updateDbObj)
        result.Value = dbObj.to_json()
    except AttributeError:
        result.AddError('This education does not exist, perhaps you wished to add it?')
    except InvalidQueryError: 
        result.AddError('Invalid field in the update statement, please review')
    except:
        result.AddError('Unknown error consult the system administrator')  
    return result.ToResponse()
@app.route('/education/<id>', methods=['DELETE'])
def DeleteEducationById(id):
    result = Result()
    try: 
        toDelete = Education.objects.filter(Id = id).first()
        toDelete.delete()
        result.Value = "Element Removed succesfully"
    except AttributeError:
        result.AddError('This education does not exist, perhaps it was already deleted?')
    return result.ToResponse()

