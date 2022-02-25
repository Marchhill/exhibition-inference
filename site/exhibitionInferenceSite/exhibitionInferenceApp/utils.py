from . import models
import time
import uuid
from django.utils.dateparse import parse_datetime

# map of device id to (session, lastReading) pairs
devices = {}
timeout = 10  # seconds, put this somewhere else not magic number!


def writeReading(x, y, z, t, session, quality):
    print("writing (" + str(x) + ", " + str(y) + ") with t=" + str(t) + " to db!")
    models.Reading(x=x, y=y, z=z, t=parse_datetime(t),
                   session=session, quality=quality)
    # get session and update endTime to t


def getSession(deviceId, timeReading):
    if deviceId in devices:
        session, t = devices[deviceId]
        now = time.time()
        if (now - t) < timeout:
            # return session and update latest receive time
            devices[deviceId][1] = now
            return session

    # create a new session
    s = models.Session(
        device=deviceId, startTime=timeReading, endTime=timeReading)
    return 69
