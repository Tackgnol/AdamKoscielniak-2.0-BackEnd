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

import Controllers.Experience 
import Controllers.Education
import Controllers.SkillGroup
import Controllers.Certificate
import Controllers.Hobby

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
    
@app.errorhandler(BadRequest)
def error_handler(error):
     return handle_bad_request(error)


if __name__ == "__main__":
     app.run()