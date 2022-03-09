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