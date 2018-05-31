from main import app
from Models.Certificate import Certificate
from GlobalAPi.Result import Result
from flask import request
import json
import mongoengine
from mongoengine.errors import InvalidQueryError

@app.route('/certificate/add', methods=['POST'])
def AddCertificate():
    result = Result()
    certificate = request.get_json(force = True)
    certificateJSON = json.dumps(certificate) 
    try:
        job = Certificate.from_json(certificateJSON)
        job.save()
        result.Value = certificate
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()

@app.route('/certificate/<id>', methods=['GET'])
def GetCertificateById(id):
    result = Result()
    try:
        certificate = Certificate.objects(Id=id)
        result.Value = certificate.first().to_json()
    except AttributeError:
        result.AddError('Certificate not found')
    except:
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()
    
@app.route('/certificate/<id>', methods=['PUT'])
def UpdateCertificateById(id):
    result = Result()
    update = request.get_json(force = True)
    try:
        dbObj = Certificate.objects.filter(Id = id).first()
        updateDbObj = dbObj.to_mongo()
        for (key,value) in update.items():
            updateDbObj[key] = value
        
        del updateDbObj['_id']
        dbObj.update(**updateDbObj)
        result.Value = dbObj.to_json()
    except AttributeError:
        result.AddError('This certificate does not exist, perhaps you wished to add it?')
    except InvalidQueryError: 
        result.AddError('Invalid field in the update statement, please review')
    except:
        result.AddError('Unknown error consult the system administrator')  
    return result.ToResponse()
@app.route('/certificate/<id>', methods=['DELETE'])
def DeleteCertificateById(id):
    result = Result()
    try: 
        toDelete = Certificate.objects.filter(Id = id).first()
        toDelete.delete()
        result.Value = "Element Removed succesfully"
    except AttributeError:
        result.AddError('This certificate does not exist, perhaps it was already deleted?')
    return result.ToResponse()

