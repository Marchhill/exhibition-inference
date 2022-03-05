from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
import json
from typing import Optional

from . import utils
from .models import Device, Session

from django.views.decorators.csrf import csrf_exempt


def index(req: WSGIRequest) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    # serve the admin page!
    return render(req, "exhibitionInferenceApp/index.html", context={
        "data": utils.getAllReadings()
    })


@csrf_exempt
def submitReading(req: WSGIRequest) -> HttpResponse:
    def _xyzWithinBounds(x: float, y: float, z: float):
        bounds = utils.getMetadataXYZBounds()
        return bounds["X_LOWER_BOUND_METRES_INC"] <= x <= bounds["X_UPPER_BOUND_METRES_INC"] and \
            bounds["Y_LOWER_BOUND_METRES_INC"] <= y <= bounds["Y_UPPER_BOUND_METRES_INC"] and \
            bounds["Z_LOWER_BOUND_METRES_INC"] <= z <= bounds["Z_UPPER_BOUND_METRES_INC"]

    # WARNING: Potentially unsafe, particularly if POSTer has to be authenticated.
    # So far, our POSTers are not authenticated in any way, so CSRF protection is not necessary.
    print("Executed")
    if req.method != "POST":
        raise Http404("Must make a POST request!")

    try:
        data = json.loads(req.body)
    except (json.JSONDecodeError):
        return HttpResponseBadRequest("Submission not in valid JSON format!")

    try:
        x = float(data["x"])
        y = float(data["y"])
        z = float(data["z"])
        t = make_aware(datetime.fromtimestamp(float(data["t"])))
        # t = make_aware(datetime.fromtimestamp(value))
        hardwareId = str(data["deviceId"])
        quality = int(data["quality"])

        print("t is {0}".format(t))

        if t is None:  # seriously malformed timestamp
            raise ValueError
    except (KeyError, ValueError) as e:
        print("Error: {0}".format(e))
        return HttpResponseBadRequest("Invalid JSON received!")

    # get or create device associated with hardware id
    device: Device = utils.getOrCreateDeviceByHardwareId(hardwareId)

    # get the active session associated with the device
    s: Optional[Session] = utils.getActiveSessionIfExists(device=device)
    if not _xyzWithinBounds(x, y, z):  # location out of bounds
        # end session if one exists
        if s:
            utils.endSession(s)
        return HttpResponseBadRequest("Submission dropped: Location out of bounds.")
    if s:
        if utils.hasExpired(s, t):
            # session has expired, end it and make a new one
            utils.endSession(s)
            s = utils.createSession(device, t)
    else:
        # no sessions active, create one
        s = utils.createSession(device, t)

    try:
        utils.writeReading(
            x=x,
            y=y,
            z=z,
            t=t,
            session=s,
            quality=quality
        )
    except IntegrityError as e:
        if e.args[0] == "UNIQUE constraint failed: exhibitionInferenceApp_reading.session_id, exhibitionInferenceApp_reading.t":
            return HttpResponseBadRequest("Submission dropped: You've submitted this already.")
        elif e.args[0] == "CHECK constraint failed: location_bounds_check":
            # BAD ERROR: shouldn't reach this!
            return HttpResponseBadRequest("Submission dropped: Location out of bounds [BAD ERROR].")

    return HttpResponse("Submission processed successfully.")


def frontdeskDeviceSelect(req: WSGIRequest) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")
    return render(req, "exhibitionInferenceApp/deviceSelect.html", context={
        "devices": sorted(utils.getAllDevices(), key=lambda d: d.hardwareId)
    })


def frontdeskDevice(req: WSGIRequest, hardwareId: str) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    d = get_object_or_404(Device, hardwareId=hardwareId)
    return render(req, "exhibitionInferenceApp/deviceManage.html", context={"device": d})


@csrf_exempt
def metadata(req: WSGIRequest) -> HttpResponse:
    # WARNING: Sorry! I (Jacky) broke this, and will come back to fixing it tonight (Sat 5 Mar)
    # WARNING: Potentially unsafe, particularly if POSTer has to be authenticated.
    # So far, our POSTers are not authenticated in any way, so CSRF protection is not necessary.

    if req.method != "POST":
        raise Http404("Must make a POST request!")

    try:
        metadata = req.POST["metadata"]
        deviceId = req.POST["id"]
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Invalid JSON received!")

    d = utils.getDeviceByPkIfExists(deviceId)
    if d:
        # update metadata
        d.metadata = metadata
        d.save()
    else:
        return HttpResponseBadRequest("Device does not exist.")

    return redirect('/device?id=' + str(d.id))

# [DONE] TODO FIX: Database becomes inconsistent if the same session (i.e. same tag device) writes to the database backwards in time (e.g. write at t=15 and then write at t=12. It'll succeed...)
# Concrete example: (new session) write t=15 succeeds and startTime=15, then write t=14 error because location out of bounds. The session will terminate with endTime=14 but startTime=15 is later than endTime=14.
# We may assume (confirmed by Fredrik and Yash) that for each tag, the location data will come in in sequence.

# TODO CHECK: Do we need database transactions? So far every modification we make are committed immediately.
