from django.db import models
from django.db.models import F, Q


class Session(models.Model):
    device = models.CharField(max_length=200)
    # these are redundant, but optimise a common query
    startTime = models.DateTimeField('start time')
    endTime = models.DateTimeField('end time', null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                # startTime < endTime; https://docs.djangoproject.com/en/4.0/topics/db/queries/#filters-can-reference-fields-on-the-model
                check=Q(startTime__lte=F("endTime")),
                name="session_startTime_before_endTime_check"
            ),
            models.UniqueConstraint(
                fields=["device", "endTime"],
                name="no_more_than_one_active_session_check"
            )
        ]

    def session_has_ended(self) -> bool:
        return self.endTime is not None

    def __str__(self):
        return f"{self.device}({self.startTime}-{self.endTime})"


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
                check=Q(x__gte=0) & Q(x__lte=10) & Q(y__gte=0) &
                Q(y__lte=10) & Q(z__gte=0) & Q(z__lte=10),
                name="location_bounds_check"
            ),
            models.UniqueConstraint(
                fields=["session", "t"], name="idempotency_check"),
        ]

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}) at t={self.t}"
