# Backend Directory Structure (Application Logic)
**Database related**:
- `migrations/`: Auto-generated files when performing database migrations. Do not create or modify these files manually.

  - The proper way to do database migrations is to modify `models.py`, then use `python3 manage.py makemigrations` and `python3 manage.py migrate` in sequence.
  - Migration rollback: \
    Each migration has a ID attached to it (e.g. "0005_metadata.py"). As an illustration, to revert the database to the point where migration 0002 is applied, run `python3 manage.py migrate exhibitionInferenceApp 0002`. To roll forward again, run `python3 manage.py migrate exhibitionInferenceApp 0005`.
  - Relevant documentation can be found [here](). For a gentler introduction, refer to [this](https://docs.djangoproject.com/en/4.0/intro/tutorial02/) tutorial.
- `models.py`: This is where the database table schemae are defined. According to Django's conventions, each table is defined as a class, and columns are defined as class variables. The `Meta` subclass in each class is where table constraints are defined.
- `utils.py`: Database code used in deployment.
- `devUtils.py`: Database code used only for testing (not for deployment). Used for generating dummy data, etc.

**Frontend related**:
- `static/exhibitionInferenceApp/`: Contains subfolders `images`, `css`, `js` (missing if nothing's in them). Here's where we store assets that are used for the website. JavaScript code goes into the `js` subfolder.
- `templates/exhibitionInferenceApp/`: Contains .html files of our website. The .html files here use Django's templates (things like `{{ variable }}` and `{% Django directive %}`), which can be thought of as extensions to HTML. 
  - Relevant Django documentation can be found [here](https://docs.djangoproject.com/en/4.0/topics/templates/) and [here](https://docs.djangoproject.com/en/4.0/ref/templates/builtins/). For a gentle introduction, refer to [this](https://docs.djangoproject.com/en/4.0/intro/tutorial03/#use-the-template-system) tutorial.
- `views.py`: Code executed to serve the website.
  - Contains 1 method for each route defined in `urls.py`
  - The method takes 1 argument: the request (`django.core.handlers.wsgi.WSGIRequest`).
  - The method must return a response (`django.http.HttpResponse`).
  - This is where methods in `utils.py` are called: to talk to the database.


**Backend related**:
- `admin.py`: Django configuration file for the admin subdomain (`localhost:8000/admin`)
- `apps.py`: Boilerplate Django configuration file
- `tests.py`: Unit tests for backend.
- `urls.py`: Django routing control + static asset management.
