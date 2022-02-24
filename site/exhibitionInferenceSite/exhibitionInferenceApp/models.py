from django.db import models

class Session(models.Model):
	device = models.CharField(max_length=200)
	#these are redundant, but optimise a common query
	startTime = models.DateTimeField('start time')
	endTime = models.DateTimeField('end time')
	
	def __str__(self):
		return self.device + ' (' + str(self.startTime) + ' - ' + str(self.endTime) + ')'

class Reading(models.Model):
	x = models.FloatField()
	y = models.FloatField()
	z = models.FloatField()
	t = models.DateTimeField('timestamp')
	session = models.ForeignKey('Session', on_delete=models.CASCADE) #if we delete session, then delete reading
	quality = models.IntegerField()

	def __str__(self):
		return '(' + str(x) + ', ' + str(y) + ', ' + str(z) + ') at t=' + str(t)