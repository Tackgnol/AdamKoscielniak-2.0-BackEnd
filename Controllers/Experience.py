from main import app
from Models.Experience import Experience
from GlobalAPi.Result import Result
from flask import request
import json
import mongoengine
from mongoengine.errors import InvalidQueryError

@app.route('/experience/add', methods=['POST'])
def AddExperience():
    result = Result()
    experience = request.get_json(force = True)
    experienceJSON = json.dumps(experience) 
    try:
        job = Experience.from_json(experienceJSON)
        job.save()
        result.Value = experience
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + err)
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
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()
    
@app.route('/experience/<id>', methods=['PUT'])
def UpdateExperienceById(id):
    result = Result()
    update = request.get_json(force = True)
    try:
        dbObj = Experience.objects.filter(Id = id).first()
        updateDbObj = dbObj.to_mongo()
        for (key,value) in update.items():
            updateDbObj[key] = value
        
        del updateDbObj['_id']
        dbObj.update(**updateDbObj)
        result.Value = dbObj.to_json()
    except AttributeError:
        result.AddError('This experience does not exist, perhaps you wished to add it?')
    except InvalidQueryError: 
        result.AddError('Invalid field in the update statement, please review')
    except:
        result.AddError('Unknown error consult the system administrator')  
    return result.ToResponse()
    