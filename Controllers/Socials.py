from main import app
from GlobalAPi.Result import Result
from Models.Social import Social
import json
import mongoengine
import sys



@app.route('/social', methods=['GET'])
def GetSocials():
    result = Result()
    try:
        socials = Social.objects()
        result.Value = socials.to_json()
    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except TypeError as e:
        print(e)
    except:
        print(sys.exc_info()[0])
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()
