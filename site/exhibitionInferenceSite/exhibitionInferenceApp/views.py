from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login as authLogin, logout as authLogout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
import json
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

from . import utils
from .models import Device, Reading, Session


#########
# INDEX #
#########

class ReadingEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Reading):
            return o.toJson()
        return json.JSONEncoder.default(self, o)


def index(req: WSGIRequest) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    if not req.user.is_authenticated:
        # If not logged in, show "Nothing to show" page
        return render(req, "exhibitionInferenceApp/unauthenticated.html", context={})
    return render(req, "exhibitionInferenceApp/index.html", context={})


#################
# VISUALISATION #
#################

@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
@permission_required(
    "exhibitionInferenceApp.visualise_reading",
    raise_exception=True
)
def visualisationDefault(req: WSGIRequest) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    sessions = utils.getAllSessionsReverseOrder()
    paginator = Paginator(sessions, 25)  # Show 25 sessions per page
    page_number = req.GET.get("page")
    sessionsPage = paginator.get_page(page_number)
    return render(req, "exhibitionInferenceApp/visualisationDefault.html", context={
        "sessionsPage": sessionsPage,
        "totalNumberOfSessions": len(sessions)
    })


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
@permission_required(
    "exhibitionInferenceApp.visualise_reading",
    raise_exception=True
)
def visualisationAll(req: WSGIRequest) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    readings: List[Reading] = utils.getAllReadings()
    return render(req, "exhibitionInferenceApp/visualisation.html", context={
        "data": json.dumps(readings, cls=ReadingEncoder)
    })


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
@permission_required(
    "exhibitionInferenceApp.visualise_reading",
    raise_exception=True
)
def visualisationStartEndQuery(req: WSGIRequest) -> HttpResponse:
    if req.method != "POST":
        raise Http404("Must make a POST request!")
    errors = []
    if parse_datetime(req.POST["start"]) is None:
        errors.append("Invalid start datetime")
    if parse_datetime(req.POST["end"]) is None:
        errors.append("Invalid end datetime")
    if len(errors) > 0:
        messages.error(req, f"{', '.join(errors)}.")
        return HttpResponseRedirect(reverse("exhibitionInferenceApp_ns:visualisation-default"))
    return HttpResponseRedirect(reverse(
        "exhibitionInferenceApp_ns:visualisation-start-end",
        args=(req.POST["start"], req.POST["end"])
    ))


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
@permission_required(
    "exhibitionInferenceApp.visualise_reading",
    raise_exception=True
)
def visualisationStartEnd(req: WSGIRequest, startTime: str, endTime: str) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    startDateTime = parse_datetime(startTime)
    endDateTime = parse_datetime(endTime)
    if startDateTime is None or endDateTime is None:
        # severely malformed datetime strings provided
        return HttpResponseBadRequest()

    readings: List[Reading] = utils.getReadingsBetween(
        startTime=startTime, endTime=endTime)
    return render(req, "exhibitionInferenceApp/visualisation.html", context={
        "data": json.dumps(readings, cls=ReadingEncoder)
    })


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
@permission_required(
    "exhibitionInferenceApp.visualise_reading",
    raise_exception=True
)
def visualisationSession(req: WSGIRequest, sessionId: int) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    readings: List[Reading] = utils.getSessionReadings(sessionId=sessionId)
    return render(req, "exhibitionInferenceApp/visualisation.html", context={
        "data": json.dumps(readings, cls=ReadingEncoder)
    })


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
@permission_required(
    "exhibitionInferenceApp.visualise_reading",
    raise_exception=True
)
def dataDefault(req: WSGIRequest) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")
    readings: List[Reading] = utils.getAllReadings()
    return render(req, "exhibitionInferenceApp/data.html", context={
        "data": json.dumps(readings, cls=ReadingEncoder)})


##################
# LOGIN / LOGOUT #
##################

def login(req: WSGIRequest):
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    if req.user.is_authenticated:
        # If already logged in, redirect to index
        return HttpResponseRedirect(reverse("exhibitionInferenceApp_ns:index"))
    return render(req, "exhibitionInferenceApp/login.html", context={})


def loginPost(req: WSGIRequest):
    if req.method != "POST":
        raise Http404("Must make a POST request!")

    username = req.POST["username"]
    password = req.POST["password"]

    user = authenticate(req, username=username, password=password)
    if user is not None:
        # actual logging in, and saving to internal sessions database
        authLogin(req, user)

        # if a ?next= was in the URL, redirect to that.
        # (adding ?next= is done by @login_required)
        # (try visiting /frontdesk/devices when logged out, then logging in, to see how this works)
        urlQueryNexts = parse_qs(urlparse(req.META["HTTP_REFERER"]).query)\
            .get("next", [None])
        if len(urlQueryNexts) == 1 and urlQueryNexts[0] is not None:
            next = urlQueryNexts[0]
            return redirect(next)
        return HttpResponseRedirect(reverse("exhibitionInferenceApp_ns:index"))
    else:
        messages.error(req, "Invalid login credentials.")
        # Redirect to same page (/login/?next=...) if ?next= is specified, otherwise go to default login page (/login/)
        return HttpResponseRedirect(req.META.get("HTTP_REFERER", reverse("exhibitionInferenceApp_ns:login")))


def logout(req: WSGIRequest):
    if req.method != "POST":
        raise Http404("Must make a POST request!")

    authLogout(req)
    return HttpResponseRedirect(reverse("exhibitionInferenceApp_ns:index"))


############
# HARDWARE #
############

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
        hardwareId = str(data["hardwareId"])
        quality = int(data["quality"])

        print("t is {0}".format(t))
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


#############
# FRONTDESK #
#############

@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
def frontdeskDeviceSelect(req: WSGIRequest) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")
    devices = sorted(utils.getAllDevices(), key=lambda d: d.hardwareId)
    activeSessions = [utils.getActiveSessionIfExists(d) for d in devices]

    return render(req, "exhibitionInferenceApp/deviceSelect.html", context={
        "devicesAndSessions": zip(devices, activeSessions)
    })


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
def frontdeskDeviceManage(req: WSGIRequest, hardwareId: str) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    d = get_object_or_404(Device, hardwareId=hardwareId)

    sOptional: Optional[Session] = utils.getActiveSessionIfExists(d)

    lastReading = utils.getLastReading(sOptional) \
        if sOptional is not None else None
    return render(req, "exhibitionInferenceApp/deviceManage.html", context={
        "hardwareId": hardwareId,
        "oldMetadata": d.metadata,
        "textboxMetadata": d.metadata,
        "activeSessionOptional": sOptional,
        "latestReading": lastReading
    })


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
@permission_required(
    "exhibitionInferenceApp.change_device",
    raise_exception=True
)
def frontdeskDeviceManageSubmit(req: WSGIRequest, hardwareId: str) -> HttpResponse:
    if req.method != "POST":
        raise Http404("Must make a POST request!")

    d = get_object_or_404(Device, hardwareId=hardwareId)
    newMetadata: str
    try:
        newMetadata = req.POST["metadata"]
    except KeyError:
        messages.error("Request was malformed. You shouldn't see this.")
        return render(req, 'exhibitionInferenceApp/deviceManage.html', context={
            "hardwareId": hardwareId,
            "oldMetadata": d.metadata,
            "textboxMetadata": newMetadata
        })

    d = Device.objects.get(hardwareId=hardwareId)
    d.metadata = newMetadata if len(newMetadata) > 0 else None
    d.save()

    messages.success(req, 'Successfully saved changes!')
    return HttpResponseRedirect(reverse("exhibitionInferenceApp_ns:frontdesk-device-manage", args=(hardwareId,)))


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
def frontdeskSessionSelect(req: WSGIRequest) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    sessions = utils.getAllSessionsReverseOrder()
    paginator = Paginator(sessions, 25)  # Show 25 sessions per page
    page_number = req.GET.get("page")
    sessionsPage = paginator.get_page(page_number)
    return render(req, "exhibitionInferenceApp/sessionSelect.html", context={
        "sessionsPage": sessionsPage
    })


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
def frontdeskSessionManage(req: WSGIRequest, sessionId: int) -> HttpResponse:
    if req.method != "GET":
        raise Http404("Must make a GET request!")

    s = get_object_or_404(Session, pk=sessionId)
    lastReading = utils.getLastReading(s)
    return render(req, "exhibitionInferenceApp/sessionManage.html", context={
        "session": s,
        # only useful if the session has ended: see sessionManage.html's logic
        "oldMetadata": s.metadata,
        # only useful if the session has ended: see sessionManage.html's logic
        "textboxMetadata": s.metadata,
        "latestReading": lastReading
    })


@login_required(login_url=reverse_lazy("exhibitionInferenceApp_ns:login"))
@permission_required(
    "exhibitionInferenceApp.change_session",
    raise_exception=True
)
def frontdeskSessionManageSubmit(req: WSGIRequest, sessionId: str) -> HttpResponse:
    if req.method != "POST":
        raise Http404("Must make a POST request!")
    print(sessionId)

    s = get_object_or_404(Session, pk=sessionId)
    newMetadata: str
    try:
        newMetadata = req.POST["metadata"]
    except KeyError:
        messages.error("Request was malformed. You shouldn't see this.")

        return render(req, "exhibitionInferenceApp/sessionManage.html", context={
            "session": s,
            # only useful if the session has ended: see sessionManage.html's logic
            "oldMetadata": s.metadata,
            # only useful if the session has ended: see sessionManage.html's logic
            "textboxMetadata": newMetadata,
            "latestReading": utils.getLastReading(s)
        })

    s.metadata = newMetadata if len(newMetadata) > 0 else None
    s.save()

    messages.success(req, 'Successfully saved changes!')
    return HttpResponseRedirect(reverse("exhibitionInferenceApp_ns:frontdesk-session-manage", args=(s.pk,)))


# [DONE] FIX: Database becomes inconsistent if the same session (i.e. same tag device) writes to the database backwards in time (e.g. write at t=15 and then write at t=12. It'll succeed...)
# Concrete example: (new session) write t=15 succeeds and startTime=15, then write t=14 error because location out of bounds. The session will terminate with endTime=14 but startTime=15 is later than endTime=14.
# We may assume (confirmed by Fredrik and Yash) that for each tag, the location data will come in in sequence.

# TODO CHECK: Do we need database transactions? So far every modification we make are committed immediately.
