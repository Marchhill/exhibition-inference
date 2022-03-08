from django.db import models
from django.db.models import F, Q
from django.contrib import admin


class Metadata(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(max_length=200)

    # Key-value pair
    def __str__(self):
        return f"{self.key}={self.value}"


class Session(models.Model):
    device = models.ForeignKey(
        'Device', on_delete=models.CASCADE, db_column='hardwareId')
    metadata = models.CharField(max_length=1000, null=True, blank=True)
    # these are redundant, but optimise a common query
    startTime = models.DateTimeField('start time')
    endTime = models.DateTimeField('end time', null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                # startTime <= endTime; https://docs.djangoproject.com/en/4.0/topics/db/queries/#filters-can-reference-fields-on-the-model
                check=Q(startTime__lte=F("endTime")),
                name="session_startTime_before_endTime_check"
            )
        ]

    @admin.display(description="Session ID")
    def admin_session_id(self) -> int:
        """
        Used only in admin.py
        """
        return self.pk

    def session_has_ended(self) -> bool:
        return self.endTime is not None

    def __str__(self):
        if self.metadata:
            return f"{self.device}({self.startTime}-{self.endTime}): {(self.metadata[:10] + '...') if len(self.metadata) > 10 else self.metadata}"
        else:
            return f"{self.device}({self.startTime}-{self.endTime})"

    def toJson(self) -> dict:
        return {
            "pk": self.pk,
            "startTime": self.startTime.isoformat(),
            "endTime": None if self.endTime is None else self.endTime.isoformat(),
            "metadata": self.metadata,
        }


class Reading(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    t = models.DateTimeField('timestamp')
    # if we delete session, then delete reading
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    quality = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(quality__gte=0) & Q(quality__lte=100),
                name="quality_bounds_check"
            ),
            models.UniqueConstraint(
                fields=["session", "t"], name="idempotency_check"),
        ]

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}) at t={self.t}"

    def toJson(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "t": self.t.isoformat(),
            "session": self.session.toJson(),
            "quality": self.quality
        }


class Device(models.Model):
    hardwareId = models.CharField(max_length=200, primary_key=True)
    # store metadata with device until session starts
    metadata = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        if self.metadata:
            return f"{self.hardwareId}: {(self.metadata[:10] + '...') if len(self.metadata) > 10 else self.metadata}"
        else:
            return self.hardwareId

    def toJson(self) -> dict:
        return {
            "id": self.pk,
            "hardwareId": self.hardwareId,
            "metadata": self.metadata,
        }
