from main import app, jwt
from Models.User import User, TokenInfo
from GlobalAPi.Result import Result
from Utils.Encryption import hashPassword, checkPassword
from Utils.UserValidation import IsUserRoleValid, IsUserAdmin
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, jwt_optional, get_jwt_claims,
    create_refresh_token, jwt_refresh_token_required
)
from flask import Flask, request
import mongoengine


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        'role': user.role,
        'Id': user.Id
    }


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
    if loggingUser is None:
        result.AddError("Invalid login or password")
        return result.ToResponse()
    userHash = loggingUser.Password
    userRole = loggingUser.AccountType
    userId = loggingUser.Id

    forToken = TokenInfo(username, userRole, userId)

    if checkPassword(password, userHash):

        access_token = create_access_token(identity=forToken)
        refresh_token = create_refresh_token(identity=forToken)
        result.Value = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    else:
        result.AddError("Invalid login or password")

    return result.ToResponse()


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    result = Result()
    username = get_jwt_identity()
    loggingUser = User.objects(Email=username).first()
    loggingUser = User.objects(Email=username).first()
    userRole = loggingUser.AccountType
    userId = loggingUser.Id

    forToken = TokenInfo(username, userRole, userId)
    if loggingUser is None:
        result.AddError("User not found/Invalid Token")
        return result.ToResponse()
    ret = {
        'access_token': create_access_token(identity=forToken),
        'refresh_token': create_refresh_token(identity=forToken)
    }
    result.Value = ret
    return result.ToResponse()


@app.route('/register', methods=['POST'])
@jwt_optional
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

    role = request.json.get('AccountType')
    currentClaim = get_jwt_claims()
    if not IsUserAdmin(currentClaim['role']):
        if not IsUserRoleValid(role):
            result.AddError('Invalid user role')
            return result.ToResponse()

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
