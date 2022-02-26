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
    """
    Helper function used within utils.py, not to be called from outside.
    Creates a new session in the database for the device. Used when device 
    sends coordinates within museum bounds, and an active session does not 
    exist yet.

    Args:
        deviceId (str): String ID of a device
        startTime (datetime): datetime object provided by the device's location
        data

    Returns:
        Session: A Session object representing the session record in the database.
    """
    s = Session(device=deviceId, startTime=startTime)
    s.save()
    return s


def getSession(deviceId: str, timeReading: datetime) -> Session:
    """
    Either retrieves an active session object from the database, or create 
    one if not exists.

    Args:
        deviceId (str): String ID of a device
        timeReading (datetime): datetime object provided by the device's 
        location data

    Returns:
        Session: A Session object representing the session record in the database.
    """
    # TODO: Potential race condition? Two incoming requests calling this method at the same time may generate 2 separate sessions...
    try:
        s: Session = Session.objects.get(device=deviceId, endTime__isnull=True)
    except Session.DoesNotExist:  # either device is new, or device's current session has terminated
        return _createNewSession(deviceId=deviceId, startTime=timeReading)

    # device's current session is still active (except clause not run)
    r: QuerySet[Reading] = Reading.objects\
        .filter(session_id=s.pk).order_by("t").reverse()[:1]
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
    """
    Terminates the active session for a device, if one exists. Otherwise,
    do nothing.

    Args:
        deviceId (str): String ID of a device
        lastSeen (datetime): datetime object provided by the device's location 
        data
    """
    try:
        s: Session = Session.objects.get(device=deviceId, endTime__isnull=True)
    except Session.DoesNotExist:  # either device is new, or device's current session has terminated
        return
    s.endTime = min(lastSeen, s.startTime + timedelta(seconds=10))
    s.save()


# TODO: Run this nightly at 2359
def nightlyEndActiveSessions() -> None:
    """
    Terminates all active sessions. To be called periodically (e.g. nightly).
    """
    activeSessions: QuerySet[Session]
    activeSessions = Session.objects.filter(endTime__isnull=True)
    for s in activeSessions:
        s.endTime = s.startTime + timedelta(seconds=10)
        s.save()
