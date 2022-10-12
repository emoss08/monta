# Monta Command Help Log

### Creating a Backup of Database entries

_________________________________________________________________________________________

1. Dump data into Json file

#### Linux / WSL

````bash
py manage.py dumpdata -- indent=2 --output=backup.json
````

#### Windows

````bash
python manage.py dumpdata -- indent=2 --output=backup.json
````

-- Additional Information --
If you get an encoding error when running the command, include the following in the command:

#### Linux / WSL

````bash
py manage.py dumpdata -- indent=2 --output=backup.json --Xutf8
````

#### Windows

````bash
python manage.py dumpdata -- indent=2 --output=backup.json --Xutf8
````

2. Load database entries from a JSON file

#### Linux / WSL

````bash
py manage.py loaddata backup.json
````

#### Windows

````bash
python manage.py loaddata backup.json
````

# Monta Reference Log

### Replacing Search Vector for search queries.

_________________________________________________________________________________________

1. Delete all search vectors (Example: monta_driver/views.py)

````python
results = Driver.objects.annotate(
    search=SearchVector(
        "driver_id",
        "first_name",
        "last_name",
        "profile__license_state",
        "profile__license_number",
        "profile__license_expiration",
    )
).filter(search=query)
````

2. Replace with the following:

````python
results = Driver.objects.filter(
    Q(driver_id__icontains=query)
    | Q(first_name__icontains=query)
    | Q(last_name__icontains=query)
    | Q(profile__license_number__icontains=query)
    | Q(profile__license_state__icontains=query)
    | Q(profile__license_expiration__icontains=query)
)
````

### Setting up PostgreSQL for Monta Search Capabilities

_________________________________________________________________________________________

1. Add pg_trgm extension to database

````sql
CREATE EXTENSION pg_trgm;
````

2. Add the following to monta_driver/views.py

````python
results = (
    Driver.objects.annotate(
        similarity=TrigramSimilarity(
            "driver_id",
            query,
        ),
    )
)
````

### Get CSRF Token for HTTP Requests with JavaScript

_________________________________________________________________________________________

1. Add the following to your JavaScript file

````javascript
<script src="//cdn.jsdelivr.net/npm/js-cookie@3.0.1/dist/js.cookie.min.js"></script>
const csrftoken = Cookies.get("csrftoken");
document.addEventlistener('DOMContentLoaded', (event) => {
    {% block domready %}
    {% endblock %}
});
````