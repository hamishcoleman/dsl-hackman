all: test

# Packages to install if we are running on Travis-CI (Ubuntu Xenial)
PACKAGES_XENIAL := \
    python3-django \
    python3-flake8 \
    python3-jinja2 \
    python3-pytest-django \
    python3-gunicorn \
    python3-coverage \
    python3-pytest \
    python3-pytest-cov \
    python3-ipy \
    python3-redis \
    python3-django-ratelimit \
    python3-django-cors-headers \
    python3-django-oauth-toolkit \
    redis-server \
    gunicorn3 \
    python3-gevent \
    flake8 \

# Packages to install if we are running on Debian
PACKAGES_DEBIAN := $(PACKAGES_XENIAL) \
    python3-django-redis \

# TODO - from the requirements.txt
# pyserial>=3.2.1
# RPi.GPIO>=0.6.3


build-depends:
	sudo apt-get install -y $(PACKAGES_DEBIAN)

build-depends-xenial:
	sudo apt-get install -y $(PACKAGES_XENIAL)

# Create or update the database
dev.db:
	python3 manage.py migrate

# Run the site with a development server
dev.run:
	python3 manage.py runserver

test.style:
	flake8

test.unit:
	env DJANGO_SETTINGS_MODULE=hackman.settings_test /usr/bin/pytest-3 --cov-report=term-missing --cov-fail-under=98 --cov=.

test: test.style test.unit
