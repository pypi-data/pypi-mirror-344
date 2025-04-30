================
django-enquiries
================

django-enquiries is a Python Django app to handle un-authenticated user enquiries via a contuct-us form.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "enquiries" to your INSTALLED_APPS setting like so::

    INSTALLED_APPS = [
        ...,
        "enquiries",
    ]

2. Include the enquiries URLconf in your project urls.py like so::

    path("enquiries/", include("enquiries.urls")),

3. Run ``python manage.py migrate`` to create the models.