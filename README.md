## (Test) Deployment Notes
How to run the website?
1. Clone this repository.
2. Install pre-requisites into your (virtual) environment: see `requirements.txt`
3. Change directory to `exhibition-inference/site/exhibitionInferenceSite/`
4. Run `python3 manage.py runserver` to serve the server on `localhost:8000`. 
5. cURL request template:\
   `curl -X POST -H "Content-Type: application/json" -d '{"x":1.2, "y":1.4, "z":1.5, "t":"2022-02-26T00:39:25.018240Z", "deviceId":"sampledevice", "quality":100}' localhost:8000/submit/` (this is a well-formed request and should succeed)
   - So far (as of commit cd4c05a (3am Sat 26 Feb), multiple constraints have been added:
     - x, y, z must all be floats within 0 and 10 inclusive
     - t must be a timestamp string (ISO 8601 format)
     - quality is an integer between 0 and 100 inclusive
     - Repeated identical requests are rejected
   - Malformed JSONs, invalid types, out of bound coordinates, malformed timestamps, etc. should all be rejected: your cURL response should tell you so.
   - **General operation**
     - The gateway devices sends, for each device and for each data (x,y,z,t), a POST request to the `/submit/` domain.
     - This creates a session for the device, only if the x,y,z coordinates are all within bounds.
     - This session ends if one of these conditions hold:
       - New data arrives with some of x,y,z out of bounds (no new session created)
       - New data arrives with a gap of more than 10s from previously saved data (new session created)
       - Nightly at 23:59:59, all sessions are ended. _(need to set up cron job or something)_

# Exhibition Inference

The Royal College of Music has one of the richest collections of music-related objects in the UK and Europe, spanning over 500 years of musical activity. A new layout has just been created, and the museum needs to learn how visitors respond to it in order to refine the design in future. 

The project aims to combine ArUco marker scan locations with dead reckoning to estimate how visitors travel around the museum, as well as how long they spend at each exhibit.
