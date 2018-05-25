from flask import Flask, request
import json
from flask_mail import Mail, Message
from Models.Experience import Experience
from GlobalAPi.Result import Result
from Config.config import Config
from GlobalAPi.Exceptions import BadRequest
from GlobalAPi.ExceptionHandlers import handle_bad_request
import mongoengine

app = Flask(__name__)

cfg = Config()

app.config['JSON_SORT_KEYS'] = False
app.config['MAIL_SERVER'] = cfg.MAIL_SERVER
app.config['MAIL_PORT'] = cfg.MAIL_PORT
app.config['MAIL_USERNAME'] = cfg.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = cfg.MAIL_PASSWORD
mail = Mail(app)
mongoengine.connect(
    db=cfg.MONGO_DB,
    username=cfg.MONGO_USERNAME,
    password=cfg.MONGO_PASSWORD,
    host=cfg.MONGO_HOST
)


@app.route("/requestForwarder/<email>", methods=['POST'])
def MailPayUResponse(email):
    payUrequestBody = request.data
    headerDict = {}
    payUrequestHeader = request.headers
    for (key,value) in payUrequestHeader:
        headerDict[key] = value

    mail.send_message(
        subject="Request was sent",
        recipients=[email],
        body=str(payUrequestBody.decode('utf-8')) + "\n" + json.dumps(headerDict),
        sender="emailMonkey@adamkoscielniak.eu.org"
        )
    return payUrequestBody 
    
    
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
    dbObj = Experience.objects.filter(Id = id).first()
    updateDbObj = dbObj.to_mongo()
    for (key,value) in update.items():
        updateDbObj[key] = value
    del updateDbObj['_id']
    dbObj.update(**updateDbObj)

    return dbObj.to_json()
    

@app.errorhandler(BadRequest)
def error_handler(error):
     return handle_bad_request(error)


if __name__ == "__main__":
     app.run()