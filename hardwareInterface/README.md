# Hardware Guide
## File breakdown
### **configure.py**
### Description
This script is used to configure the tags, anchors and the single passive device. It requires a wired connection.
### Usage
- Make sure that the device (e.g. tag) is connected using a micro-usb cable to the computer running this script
- `cd .../exhibition-inference/hardwareInterface/`
- `python3 configure.py`
- Follow instructions as prompted in the terminal

### **passive.py**
### Description
This is responsible for gathering the data from a maximum of 5 tags concurrently and sending it to the database. Ensure that the database server is running before running this script. This script requires a bluetooth connection to the **passive** device.
### Usage
- Ensure that the database server is running. It can be started like so:
    - `cd .../exhibition-inference/site/exhibitionInferenceSite`
    - `python3 manage.py runserver`
    - As a sidenote, one can now access the visualisation interface by navigating to `http://127.0.0.1:8000/` in the browser
    - The admin interface can be reached by navigating to `http://127.0.0.1:8000/admin` in the browser and using `delta_admin` as **both** the username and the password
- Make sure that the **passive** device is discoverable via bluetooth i.e. it is not too far away from the computer running this script. Also ensure that the computer running this script is capable of connecting to bluetooth devices.
- `cd .../exhibition-inference/hardwareInterface/`
- `python3 passive.py <English name of **passive** device`>


### **getIDs.py**
### Description
This is used to get the 8-byte node ID, along with the shortened 2-byte node ID of the device. This 2-byte node ID corresponds to the lower 2-bytes (4 hex digits) of the 8-byte version. It requires a bluetooth connection.
### Usage
- Make sure that the device (e.g. tag) is discoverable via bluetooth i.e. it is not too far away from the computer running this script. Also ensure that the computer running this script is capable of connecting to bluetooth devices.
- `cd .../exhibition-inference/hardwareInterface/`
- `python3 getIDs.py <names of devices you wish to get IDs of>`. For example, if you want to get the IDs for Tag1 and the anchor Blue: `python3 getIDs.py Tag1 Blue`

### **main.py**
### Description
This script is no longer needed, but can be used for debugging. It can be used to connect to a **tag** and access distance information of the tag to each of the anchors. Depending on the data mode of the tag (0: Position, 1: Distances, 2: Positions + Distances), it prints different information to the console. In mode 0, tuples of the form (X, Y, Z, quality) will be printed. In mode 1, tuples of the form (hex(node_id), distance, quality) will be printed. In mode 2, tuples of both forms will be printed.
### Usage
- Make sure that the tag is discoverable via bluetooth i.e. it is not too far away from the computer running this script. Also ensure that the computer running this script is capable of connecting to bluetooth devices.
- `cd .../exhibition-inference/hardwareInterface/`
- `python3 main.py <English name of tag>`

## Moving the anchors around

- The anchors need not be in any specific shape, but it is recommended that a rectangle is used for ease of configuration.
- >It is very important that all the anchors are not coplanar. It is recommended to have 3 tags high-up on the ceiling and one near the floor. If all the tags are coplanar, then the z-axis information will not entirely useful as although it will tell you the correct distance of the tags from the plane defined by the anchors, you will not be able to tell if the tag is above the anchor plane or below. This corresponds to not being able to detect if people are walking on the museum floor or have travelled above it.
- Note down the positions of the anchors **relative to the room origin**. It is vital that these positions are relative to the room origin for the system to work correctly and the data generated to still be compatible with old data (with the old anchor positions).
- Configure the anchors using the configuration script
- Place the anchors in the room according to the positions noted down before
- Navigate to `http://127.0.0.1:8000/admin` (after starting the server - process described in the passive.py section above)
- Configure the bounds using the *My actions* section on the right. These bounds correspond to the dimensions of the room (the area in which we want to track people) **relative to the room origin**


## Troubleshooting
### Device configuration
Ensure that when configuring the device, the USB cable is securely plugged in and that the battery is inside the device.
### No data written to the database
One reason for this maybe improper configuration of the bounds. Bounds are used to segment different sessions automatically. Ensure that the bounds correspond correctly to the placement of the anchors in the room.

## Terminology
### Room origin:
An arbitrary point from which all physical distance measurements are taken from and tracking data corresponds to.
