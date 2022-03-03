from datetime import datetime, timedelta
from django.db.models import QuerySet
from typing import Dict, List
from .models import Metadata, Session, Reading, Device


# Metadata
def getMetadataTimeoutInSeconds() -> int:
    return int(Metadata.objects.get(key="TIMEOUT_IN_SECONDS").value)


def getMetadataXYZBounds() -> Dict[str, float]:
    data = Metadata.objects.filter(key__endswith="BOUND_METRES_INC")
    return {m.key: float(m.value) for m in data}

# Reading


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


def getAllReadings() -> List[Reading]:
    return [e for e in Reading.objects.all()]


def _lastReading(session: Session) -> datetime:
    """
    Helper function that should only be used inside utils
    Finds the last reading associated with the session

    Args:
        session (Session): A Session object representing the session record in the database

    Returns:
        datetime: Time object of last reading
    """
    r: QuerySet[Reading] = Reading.objects\
        .filter(session_id=session.pk).order_by("t").reverse()

    if len(r) == 0:
        return None
    else:
        return r[0]

# Device


def getDeviceByHardwareId(hardwareId: str) -> Device:
    try:
        return Device.objects.get(hardwareId=hardwareId)
    except Device.DoesNotExist:
        return None


def getDevice(deviceId: str) -> Device:
    try:
        return Device.objects.get(pk=deviceId)
    except Device.DoesNotExist:
        return None


def getAllDevices() -> List[Device]:
    return [e for e in Device.objects.all()]


def createDevice(hardwareId: str) -> Device:
    """
    Create a new hardware device

    Args:
        hardwareId (str): string identifier of device

    Returns:
        Device: A Device object representing the device in the database
    """
    d = Device(hardwareId=hardwareId)
    d.save()
    return d

# Session


def createSession(device: Device, startTime: datetime) -> Session:
    """
    Creates a new session in the database for the device. Used when device 
    sends coordinates within museum bounds, and an active session does not 
    exist yet.

    Args:
        device (Device): A Device object representing the device in the database
        startTime (datetime): datetime object provided by the device's location
        data

    Returns:
        Session: A Session object representing the session record in the database
    """
    s = None
    s = Session(device=device, startTime=startTime)
    s.save()
    return s


def getSession(device: Device) -> Session:
    """
    Retrieves an active session object from the database if one exists

    Args:
        device (Device): A Device object representing the device in the database.
        timeReading (datetime): datetime object provided by the device's 
        location data

    Returns:
        Session: A Session object representing the session record in the database
    """

    try:
        return Session.objects.get(device_id=device.pk, endTime__isnull=True)
    except Session.DoesNotExist:  # either device is new, or device's current session has terminated
        return None


def hasExpired(session: Session, timeReading: datetime) -> bool:
    """
    Checks if the given session has expired by the time of the reading

    Args:
        session (Session): A Session object representing the session record in the database
        timeReading (datetime): Time object that represents when the reading occured

    Returns:
        bool: has the session expired?
    """
    # find last reading
    lastReading = _lastReading(session)

    if not lastReading:
        # no associated reading found (should never happen)
        return True
    else:
        # test for timeout
        return (timeReading - lastReading.t).total_seconds() > getMetadataTimeoutInSeconds()


def endSession(session: Session) -> None:
    """
    Ends the given session, giving it an end time and metadata

    Args:
        session (Session): A Session object representing the session record in the database
    """
    # find last reading
    lastReading = _lastReading(session)

    if not lastReading:
        # no associated reading found (should never happen)
        session.endTime = session.startTime
    else:
        # terminate device current session and start a new one
        session.endTime = lastReading.t

    device = getDevice(session.device_id)

    # if device has metadata transfer it to the session and remove from device
    if device.metadata:
        session.metadata = device.metadata
        device.metadata = None
        device.save()

    session.save()

# TODO: Run this nightly at 2359


def nightlyEndActiveSessions() -> None:
    """
    Terminates all active sessions. To be called periodically (e.g. nightly).
    """
    activeSessions: QuerySet[Session]
    activeSessions = Session.objects.filter(endTime__isnull=True)
    for s in activeSessions:
        endSession(s)
