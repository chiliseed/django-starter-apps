Django Starter Applications
===========================

This repo contains different dockerized django starter projects, with basic use cases.

Locally, you can run the code with django compose or use our helper tool `ddc-shob <https://github.com/chiliseed/django-compose-shob>`_.

Remotely, you can use our `Chiliseed service <https://chiliseed.com>`_ to run it on AWS.

Content
-------

- **master** -> contains basic project, with:
    - multi-stage docker build setup
    - PostgreSQL db
    - pytest
    - `django-configurations <https://pytest-django.readthedocs.io/en/latest/configuring_django.html>`_
    - `django-environ <https://django-environ.readthedocs.io/en/latest/>`_
    - `django rest framework <https://www.django-rest-framework.org/>`_
    - `django-healthcheck <https://pypi.org/project/django-health-check/>`_
    - example template based app
    - `django-extensions <https://django-extensions.readthedocs.io/en/latest/>`_ for local environment
    - `django-storages <https://django-storages.readthedocs.io/en/latest/>`_ with S3 backend setup
    - `django-structlog <https://github.com/jrobichaud/django-structlog>`_
- **cache** -> basic project + redis cache
- **offline-workers** -> basic project + redis cache + celery configured to run with redis broker


How to use
----------

1. Clone this repo locally
2. Rename upper most folder to something meaningful to you
3. Optionally, recommended, update packages in ``requirements`` folder to latest versions
4. Rename ``container_name`` in ``docker_compose.yml`` to something meaningful to you
5. Rename network in ``docker_compose.yml`` to something meaningful to you
6. ``cp .env.template .env`` and fill in the blanks
7. You might also want to remove the ``LICENSE``, unless your project is also open source and MIT license is good for you
8. ``ddc-shob start`` and see your project being setup and started


Issues and features suggestions
-------------------------------

Please open a ticket with relevant details.
