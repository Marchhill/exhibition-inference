## (Test) Backend Deployment Notes

**How to run the backend server?**

1. Clone this repository.
2. Install pre-requisites into your (virtual) environment: see `exhibition-inference/requirements.txt`
3. Change directory to `exhibition-inference/site/exhibitionInferenceSite/`
4. Run `python3 manage.py runserver` to serve the server on `localhost:8000`. 
5. To manually send POST requests to the server, use this cURL request template on your CLI:\
   `curl -X POST -d '{"x":1.2, "y":1.4, "z":1.5, "t":"2022-02-26T00:39:25.018240Z", "deviceId":"sampledevice", "quality":100}' localhost:8000/submit/` (change the stuff after `-d`; this is a well-formed request and should succeed)

   `curl -X POST -d "{\"x\":1.2, \"y\":1.4, \"z\":1.5, \"t\":\"2022-02-26T00:39:25.018240Z\", \"deviceId\":\"sampledevice\", \"quality\":100}" localhost:8000/submit/` (Windows friendly version)

   - `site/exhibitionInferenceSite/exhibitionInferenceApp/devUtils.py` contains some code that does automatic POST requests via Python, which can be useful.
   - So far (as of commit cd4c05a (3am Sat 26 Feb), multiple constraints have been added:
     - x, y, z must all be floats within 0 and 10 inclusive
     - t must be a timestamp string (ISO 8601 format)
     - quality is an integer between 0 and 100 inclusive
     - Repeated identical requests are rejected
   - Malformed JSONs, invalid types, out of bound coordinates, malformed timestamps, etc. should all be rejected: your cURL response should tell you so.

**General operation**

- The backend server will be hosted on the gateway device.
- The gateway receives from each tag data of the form (x,y,z,t, tag_device_id, quality). For each data tuple, a POST request is sent to the backend's `/submit/` domain.
- This creates a session for the tag (with non-empty startTime, empty endTime), only if the x,y,z coordinates are all within bounds.
- All data that arrives from this tag from now on will be marked under the same session (unique session ID), provided they're sent within a preset timeout (10s for now).
- This tag's session ends (with non-empty endTime) if one of these conditions hold:
  - New data arrives from the tag with some of x,y,z out of bounds (no new session is created)
  - New data arrives from the tag with a gap of more than 10s from previous data (also causes new session to be created)
  - Nightly at 23:59:59, all sessions are ended. _(need to set up cron job or something)_

**For development/testing: How to interact with the database (add/view/modify records directly)?**

Either:
- Use a program to open the db.sqlite3 file directly (e.g. DB Browser for SQLite)
- Run the website as above, then go to `localhost:8000/admin/` and login with username=password=`delta_admin`.

# Exhibition Inference

The Royal College of Music has one of the richest collections of music-related objects in the UK and Europe, spanning over 500 years of musical activity. A new layout has just been created, and the museum needs to learn how visitors respond to it in order to refine the design in future. 

The project aims to combine ArUco marker scan locations with dead reckoning to estimate how visitors travel around the museum, as well as how long they spend at each exhibit.
