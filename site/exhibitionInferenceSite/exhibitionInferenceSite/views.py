from django.http import HttpResponse, HttpResponseServerError, Http404
from django.template import loader
import json

#takes list of 3 pairs in form (distance, anchor location {x, y})
def triangulate(anchors):
	if len(anchors) != 3:
		return None
	
	#carry out triangulation
	return (69., 69.)

def writeReading(x, y, t):
	print("writing (" + str(x) + ", " + str(y) + ") with t=" + str(t) + " to db!")

def index(req):
	template = loader.get_template('index.html')
	#serve the admin page!
	return HttpResponse(template.render({}, req))

def submitReading(req):
	#add a reading to the database
	if req.method == 'POST':
		data = {}
		try:
			data = json.loads(req.body)
		except:
			HttpResponseServerError("Submission not in valid JSON format!")
		
		anchors = []
		for ident, dist in data['distances'].items():
			#if identifier is a beacon, add pair (dist, anchor location) to anchors
			pass
		x, y = triangulate(anchors)

		#write x, y to database
		writeReading(x, y, data['time'])

		return HttpResponse("Submission processed.")
	
	raise Http404("Must make a POST request!")