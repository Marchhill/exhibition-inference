from django.http import HttpResponse, HttpResponseServerError, Http404
from django.template import loader
import json
from . import utils


def index(req):
    template = loader.get_template('index.html')
    # serve the admin page!
    return HttpResponse(template.render({}, req))


def submitReading(req):
    # add a reading to the database
    if req.method == 'POST':
        data = {}
        try:
            data = json.loads(req.body)
        except:
            HttpResponseServerError("Submission not in valid JSON format!")

        x = data['x']
        y = data['y']
        z = data['z']
        t = data['t']
        deviceId = data['deviceId']
        quality = data['quality']
        sessionId = getSessionId(deviceId, t)

        # write x, y to database
        writeReading(x, y, z, t, sessionId, deviceId, quality)

        return HttpResponse("Submission processed.")

    raise Http404("Must make a POST request!")
