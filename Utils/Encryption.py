from bcrypt import hashpw, checkpw, gensalt
from Config.config import Config

def hashPassword(password):
    cfg = Config()
    hashed = hashpw(password.encode('utf-8'), gensalt(cfg.SaltNo))
    return hashed

def checkPassword(plainTextPass, hashPass):
    encodedPass = plainTextPass.encode('utf-8')
    encodedHash = hashPass.encode('utf-8')
    return checkpw(encodedPass, encodedHash)