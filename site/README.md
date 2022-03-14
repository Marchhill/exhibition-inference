**Directory Structure**
- `exhibitionInferenceSite`: rest of the backend
- `scripts`: contains scripts used in development only. `devUtils.py` was used to populate the database (`exhibitionInferenceSite/db.sqlite3`) with random data.

# High level description of data collection procedure

- The backend server will be hosted on the Raspberry Pi.
- The passive device receives from each tag data of the form (x,y,z,t, tag_device_id, quality). For each data tuple, a POST request is sent to the backend's `/submit/` domain.
- This creates a session for the tag (with non-empty startTime, empty endTime), only if the x,y,z coordinates are all within bounds.
- All data that arrives from this tag from now on will be marked under the same session (unique session ID), provided they're sent within a preset timeout (10s for now).
- This tag's session ends (with non-empty endTime) if one of these conditions hold:
  - New data arrives from the tag with some of x,y,z out of bounds (no new session is created)
  - New data arrives from the tag with a gap of more than 10s from previous data (also causes new session to be created)

# Deployment Notes
To deploy on the Raspberry Pi:
1. Establish connection to the Raspberry Pi.\
   The Pi has been configured to automatically connect to the SSID=`Museum` WiFi automatically on booting up (receiving power).\
   On another device (e.g. laptop) also connected to the same WiFi SSID:
   - Run `ping raspberrypi.local` in a terminal to discover the (site-local) IP address of the Pi. If it helps, the MAC address of the Pi is `E4:5F:01:7F:BC:72`. For more help, go to [Raspberry Pi's official documentation](https://www.raspberrypi.com/documentation/computers/remote-access.html#ip-address).
   - Run `ssh pi@<ip>`, keying in the IP address you found in the previous step. You'll be prompted for Pi's password: use [redacted].
2. Pull changes from this Github and redeploy.\
   Run this command:\
     `wget --no-cache -O setupPi.sh https://raw.githubusercontent.com/Marchhill/exhibition-inference/main/setupPi.sh; chmod +x setupPi.sh; sudo ./setupPi.sh;`.\
    The setup process will run automatically. Once it succeeds, the backend is successfully deployed. The output will give you the IP address which can be used by devices on the WiFi LAN to access the backend website.
    
    > What is done on first run:
    > - Create a directory `/deltaForce` on the Pi
    > - Pulls the latest version of the main branch of this repository into that directory
    > - Installs all dependencies
    > - Instates a new database (replacing any older copies)
    > - Installation and deployment
    >
    > What is done on subsequent runs:
    > - The existing database is copied to `/deltaForceDBBackups`.\
    >   _There is no code to merge these backups together: that's dependent on future use cases, which we cannot predict now. There's a possiblity of non-backwards-compatible database migrations, so we can't assume old and new databases are merge-able. We only copy backup._
    > - The `/deltaForce` directory is deleted, and everything runs as though it's the first run.
    > 
    > No interaction from the user is required; the `setupPi.sh` file is designed to complete automatically.

To deploy on an Ubuntu machine (something like your Desktop computer / laptop):
1. Pull changes from this Github and redeploy.\
   Run this command:\
     `wget --no-cache https://raw.githubusercontent.com/Marchhill/exhibition-inference/main/setupUbuntuDeployment.sh;`\
     **This file has to run with sudo permissions; it might be useful to read the file first before executing it:**\
     `chmod +x setupUbuntuDeployment.sh; sudo ./setupUbuntuDeployment.sh;`\
   _The philosophy and inner mechanics are the same as deploying on a Pi, except a minor difference with installing NGINX (the Pi uses Debian which has different packages from Ubuntu)._
   

# Development Notes
_Mainly intended for the students working on this project, and those maintaining this codebase._

The backend server has a development mode. To deploy new features, use this section to add new code/features, then push to the `main` branch, then use [Deployment Notes](#deployment-notes) to deploy.

_Caveats of deployment server: This server can only be seen via localhost. Other devices on your LAN cannot access this website. For that, you need a [deployment server](#deployment-notes)._

**Running development server on localhost:**

1. Clone this repository.
2. Install pre-requisites into your (virtual) environment: see `exhibition-inference/requirements.txt`
3. Change directory to `exhibition-inference/site/exhibitionInferenceSite/`
4. Run `python3 manage_development.py runserver` to serve the server on `localhost:8000`. 
5. To manually send POST requests to the server, use this cURL request template on your CLI:\
   `curl -X POST -d '{"x":1.2, "y":1.4, "z":1.5, "t":"2022-02-26T00:39:25.018240Z", "hardwareId":"Tag8", "quality":100}' localhost:8000/submit/` (change the stuff after `-d`; this is a well-formed request and should succeed)

   `curl -X POST -d "{\"x\":1.2, \"y\":1.4, \"z\":1.5, \"t\":\"2022-02-26T00:39:25.018240Z\", \"hardwareId\":\"Tag8\", \"quality\":100}" localhost:8000/submit/` (Windows friendly version)

   - `site/exhibitionInferenceSite/exhibitionInferenceApp/devUtils.py` contains some code that does automatic POST requests via Python, which can be useful.
   - Multiple constraints are enforced:
     - x, y, z must all be floats within 0 and 10 inclusive
     - t must be a timestamp string (ISO 8601 format)
     - quality is an integer between 0 and 100 inclusive
     - Repeated identical requests are rejected
   - Malformed JSONs, invalid types, out of bound coordinates, malformed timestamps, etc. should all be rejected: your cURL response should tell you so.


**How to interact with the database (add/view/modify records directly)?**
- Use a program to open the db.sqlite3 file directly (e.g. DB Browser for SQLite)
- Run the website as above, then go to `localhost:8000/admin/` and login with username=password=`delta_admin`.

**Login credentials**
- username=password=`delta_admin` (used for admins, unrestricted rights)
- username=password=`frontdesk` (used for frontdesk staff to write notes for tag sessions)
- username=password=`analysis` (used for people to see visualisation data)
