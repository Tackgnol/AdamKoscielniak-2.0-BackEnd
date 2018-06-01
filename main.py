from flask import Flask, request
import json
from flask_mail import Mail, Message
from Utils.Encryption import hashPassword, checkPassword
from Models.Experience import Experience
from Models.User import User,TokenInfo
from GlobalAPi.Result import Result
from Config.config import Config
from GlobalAPi.Exceptions import BadRequest
from GlobalAPi.ExceptionHandlers import handle_bad_request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import mongoengine

app = Flask(__name__)

jwt = JWTManager(app)

import Controllers.Experience 
import Controllers.Education
import Controllers.SkillGroup
import Controllers.Certificate
import Controllers.Hobby

cfg = Config()
app.config['JWT_SECRET_KEY'] =  cfg.JWT_SECRET
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
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user.role}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

@app.route('/login', methods=['POST'])
def login():
    result = Result()
    if not request.is_json:
        result.AddError("Missing JSON in request")

    username = request.json.get('Email', None)
    password = request.json.get('Password', None)
    if not username:
       result.AddError("Missing username parameter")
    if not password:
        result.AddError("Missing password parameter")

    loggingUser = User.objects(Email=username).first()

    userHash = loggingUser.Password
    userRole = loggingUser.AccountType

    forToken = TokenInfo(username, userRole)

    if checkPassword(password, userHash):

        access_token = create_access_token(identity=forToken)
        result.Value = access_token

    else:
        result.AddError("Invalid login or password")

    return result.ToResponse()

@app.route('/register', methods=['POST'])
def register():
    result = Result()
    if not request.is_json:
        result.AddError("Missing JSON in request")
    username = request.json.get('Email', None)
    password = request.json.get('Password', None)
    if not username:
        result.AddError("Missing username parameter")
    if not password:
        result.AddError("Missing password parameter")

    hashedPassword = hashPassword(password)
    userDict = request.get_json()

    userDict['Password'] = hashedPassword

    try:
        newUser = User(**userDict)
        newUser.save()
        result.Value = "User succefully registered"

    except mongoengine.errors.NotUniqueError:
        result.AddError("Email is not unique")
    except mongoengine.errors.FieldDoesNotExist as e:
        result.AddError("Field does not exist, Details: " + str(e))
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))

    return result.ToResponse()





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
    
@app.errorhandler(BadRequest)
def error_handler(error):
     return handle_bad_request(error)


if __name__ == "__main__":
     app.run()