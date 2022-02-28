# Backend Directory Structure
The backend server is run on Django. If you're unfamiliar with Django, you may find [this](https://docs.djangoproject.com/en/4.0/intro/tutorial01/) official tutorial useful.
- `exhibitionInferenceApp/`: Application logic.
- `exhibitionInferenceSite/`: Purely boilerplate code to get the website running. No application logic is in here.
- `db.sqlite3`: Current version of the database. Contains dummy data.
- `db.sqlite3.bak`: Original version of the database, no data is in it. 
- `manage.py`: Django main engine, used to run (`python3 manage.py runserver`) and manage the server