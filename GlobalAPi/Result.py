import json
from .Exceptions import BadRequest

class Result:
    def __init__(self):
        self.Errors = []
        self.Warnings = []
        self.Infos = []
        self.Value = None
        self.IsError = False,
        self.IsWarning = False,
        self.IsInfo = False

    def AddError(self, message):
        self.Errors.append(message)
        self.IsError = True
    
    def AddWarning(self, message):
        self.Warnings.append(self, message)
        self.IsWarning = True
    
    def AddInfo(self, message): 
        self.Infos.append(self, message)
        self.IsInfo = True

    def ToResponse(self):
        responseDict = {
            'IsError': self.IsError,
            'IsWarning': self.IsWarning,
            'IsInfo': self.IsInfo,
            'Errors' : self.Errors,
            'Warnings' : self.Warnings,
            'Infos': self.Infos,
            'Value': self.Value,
        }
        if len(self.Errors) > 0:
            raise(BadRequest("There are errors in the query", payload=responseDict))
        return json.dumps(responseDict)

