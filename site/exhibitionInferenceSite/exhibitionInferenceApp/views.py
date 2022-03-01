from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
import json

from .models import Reading
from . import utils

from django.views.decorators.csrf import csrf_exempt


def index(req: WSGIRequest):
    class ReadingEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Reading):
                return o.toJson()
            return json.JSONEncoder.default(self, o)

    # serve the admin page!
    return render(req, "exhibitionInferenceApp/index.html", context={
        "data": json.dumps(utils.getAllReadings(), cls=ReadingEncoder)
    })


def _xyzWithinBounds(x: float, y: float, z: float):
    bounds = utils.getMetadataXYZBounds()
    return bounds["X_LOWER_BOUND_METRES_INC"] <= x <= bounds["X_UPPER_BOUND_METRES_INC"] and \
        bounds["Y_LOWER_BOUND_METRES_INC"] <= y <= bounds["Y_UPPER_BOUND_METRES_INC"] and \
        bounds["Z_LOWER_BOUND_METRES_INC"] <= z <= bounds["Z_UPPER_BOUND_METRES_INC"]


@csrf_exempt
def submitReading(req: WSGIRequest):
    # WARNING: Potentially unsafe, particularly if POSTer has to be authenticated.
    # So far, our POSTers are not authenticated in any way, so CSRF protection is not necessary.

    # add a reading to the database
    if req.method != "POST":
        raise Http404("Must make a POST request!")

    try:
        data = json.loads(req.body)
        x = float(data["x"])
        y = float(data["y"])
        z = float(data["z"])
        t = parse_datetime(data["t"])
        deviceId = str(data["deviceId"])
        quality = int(data["quality"])

        if t is None:  # seriously malformed timestamp
            raise ValueError
        if not _xyzWithinBounds(x, y, z):  # location out of bounds
            utils.endSessionIfExists(deviceId=deviceId, lastSeen=t)
            return HttpResponseBadRequest("Submission dropped: Location out of bounds.")
    except (json.JSONDecodeError):
        return HttpResponseBadRequest("Submission not in valid JSON format!")
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Invalid JSON received!")

    try:
        utils.writeReading(
            x=x,
            y=y,
            z=z,
            t=t,
            session=utils.getSession(deviceId, t),
            quality=quality
        )
    except IntegrityError as e:
        if e.args[0] == "UNIQUE constraint failed: exhibitionInferenceApp_reading.session_id, exhibitionInferenceApp_reading.t":
            return HttpResponseBadRequest("Submission dropped: You've submitted this already.")
        elif e.args[0] == "CHECK constraint failed: location_bounds_check":
            return HttpResponseBadRequest("Submission dropped: Location out of bounds [BAD ERROR].")

    return HttpResponse("Submission processed successfully.")

# [DONE] TODO FIX: Database becomes inconsistent if the same session (i.e. same tag device) writes to the database backwards in time (e.g. write at t=15 and then write at t=12. It'll succeed...)
# Concrete example: (new session) write t=15 succeeds and startTime=15, then write t=14 error because location out of bounds. The session will terminate with endTime=14 but startTime=15 is later than endTime=14.
# We may assume (confirmed by Fredrik and Yash) that for each tag, the location data will come in in sequence.

# TODO CHECK: Do we need database transactions? So far every modification we make are committed immediately.
