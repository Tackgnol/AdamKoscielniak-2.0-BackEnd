import json
from .Exceptions import BadRequest


class Result:
    def __init__(self):
        self.Errors = []
        self.Warnings = []
        self.Value = None

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
            'Errors': self.Errors,
            'Warnings': self.Warnings,
            'Value': json.loads(self.Value),
        }
        if len(self.Errors) > 0:
            raise(BadRequest("There are errors in the query", payload=responseDict))
        return json.dumps(responseDict)
