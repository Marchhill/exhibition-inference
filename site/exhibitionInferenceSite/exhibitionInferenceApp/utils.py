from datetime import datetime, timedelta
from django.db.models import QuerySet
from .models import Session, Reading

TIMEOUT_IN_SECONDS = 10  # put this somewhere else not magic number!


def writeReading(x: float, y: float, z: float, t: datetime, session: Session, quality: int):
    print(f"writing ({x}), {y}) with t={t} to db!")
    Reading(
        x=x,
        y=y,
        z=z,
        t=t,
        session=session,
        quality=quality
    ).save()


def _createNewSession(deviceId: str, startTime: datetime) -> Session:
    s = Session(device=deviceId, startTime=startTime)
    s.save()
    return s


def getSession(deviceId: str, timeReading: datetime) -> Session:
    # TODO: Potential race condition? Two incoming requests calling this method at the same time may generate 2 separate sessions...
    try:
        s: Session = Session.objects.get(device=deviceId, endTime__isnull=True)
    except Session.DoesNotExist:  # either device is new, or device's current session has terminated
        return _createNewSession(deviceId=deviceId, startTime=timeReading)

    # device's current session is still active (except clause not run)
    r = Reading.objects.filter(session_id=s.pk).order_by("t").reverse()
    if len(r) != 0:
        # test for timeout
        previousReading: Reading = r[0]
        if timeReading.second - previousReading.t.second > TIMEOUT_IN_SECONDS:
            # terminate device current session and start a new one
            s.endTime = previousReading.t + timedelta(seconds=10)
            s.save()
            # recursion to remove odd case where Session table contains more than 1 endTime__isnull=True entries
            return getSession(deviceId, timeReading)

    return s


def endSessionIfExists(deviceId: str, lastSeen: datetime) -> None:
    try:
        s: Session = Session.objects.get(device=deviceId, endTime__isnull=True)
    except Session.DoesNotExist:  # either device is new, or device's current session has terminated
        return
    s.endTime = min(lastSeen, s.startTime + timedelta(seconds=10))
    s.save()


# TODO: Run this nightly at 2359
def nightlyEndActiveSessions() -> None:
    activeSessions: QuerySet[Session]
    activeSessions = Session.objects.filter(endTime__isnull=True)
    for s in activeSessions:
        s.endTime = s.startTime + timedelta(seconds=10)
        s.save()
