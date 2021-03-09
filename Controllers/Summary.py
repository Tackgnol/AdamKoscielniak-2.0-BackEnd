from main import app
from GlobalAPi.Result import Result
from flask import request
import json
import mongoengine
import sys
from Controllers.Experience import TotalTimeWorked, TotalWorkProjects
from Controllers.SkillGroup import SkillCount


@app.route('/summary/counts', methods=['GET'])
def GetCounts():
    result = Result()
    expFrom = request.args.get('from') if request.args.get(
        'from') is not None else '1988-01-01'
    expTo = request.args.get('to') if request.args.get(
        'to') is not None else '3000-01-01'
    expSkills = request.args.get('skills').split(',') if request.args.get(
        'skills') is not None else []

    try:
        timeWorked = TotalTimeWorked(expFrom, expTo, expSkills)
        projectsWorked = TotalWorkProjects(expFrom, expTo, expSkills)
        skills = SkillCount()
        result.Value = json.dumps(
            [{
                'faIcon': 'fa-medal',
                'count': skills,
                'name': 'Skills'
            },
                {
                'faIcon': 'fa-clock',
                'count': timeWorked,
                'name': 'Working Hours'
            },
                {
                'faIcon': 'fa-list-ul',
                'count': projectsWorked,
                'name': 'Completed projects'
            },
                {
                'faIcon': 'fa-file-alt',
                'count': 4,
                'name': 'Certificates'
            }]
        )

    except mongoengine.errors.ValidationError as e:
        for (field, err) in e.to_dict().items():
            result.AddError(field + " : " + str(err))
    except TypeError as e:
        print(e)
    except:
        print(sys.exc_info()[0])
        result.AddError('Unknown error consult the system administrator')

    return result.ToResponse()
