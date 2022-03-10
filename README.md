# Exhibition Inference

The Royal College of Music has one of the richest collections of music-related objects in the UK and Europe, spanning over 500 years of musical activity. A new layout has just been created, and the museum needs to learn how visitors respond to it in order to refine the design in future. 

The project aims to use UWB trilateration to estimate how visitors travel around the museum, as well as how long they spend at each exhibit.

# Directory Structure
- `hardwareInferface`, `scripts`: Code that interfaces directly with hardware
- `site`: Code that runs the backend server, and the frontend visualisation code.

# Deployment Notes
There are 2 important parts to deploy: hardware, backend (which encompasses the visualisation frontend).
- For hardware deployment notes, see `hardwareInferface/README.md`.
- For backend deployment notes, see `site/README.md`.

# Navigating the website
Upon entering the website the user will see a blank screen, with an option to login in the top right.
Clicking on this will prompt the user to enter their credentials, the current credentials are as follows:
- username=password=delta_admin (used for admins, unrestricted rights)
- username=password=frontdesk (used for frontdesk staff to write notes for tag sessions)
- username=password=analysis (used for people to see visualisation data)
After logging in the user will see a basic description of the museum as well as multiple options in the top left.
## Manage devices
This allows the user to look at the current devices in the system and check if they are active or not, as well as letting them edit the metadata.
## Manage Sessions
This lets the user see all active and completed sessions in the database. Clicking on these will show information about the session, as well as allowing the user to edit metadata about that session.
## Visualisation
The user will see a list of ways they can see the data, the top option will show them all of the data on the system, the second allows them to enter the earliest StartTime and latest EndTime they want to see (in yyyy-mm-ddThh:mm:ss format). The bottom lets them pick a single session to visualise. The user then sees the data they chose on the visualisation page.
- The user will initially see a map of the museum, and all paths on the system will be mapped on it. Each path will have a different colour and at each point recorded by the system there will be an arrow pointing towards the next arrow.
- The button "Forwards" makes it so the user can only see a single path, the next one in the list of paths.
- "Backwards" will go back in the list of paths.
- "See All" Lets the user see all of the points on the map again, like when the loaded the page.
- "Animate!" shows an animation of all of the paths currently visible on the map, how fast they move is directly related to how fast the tag moved.
- Filters on data can be made by using entering subpaths into the search bar as detailed on the screen.
## Data
The user will be able to see the raw data, so they can export it and use it however they feel appropriate.
