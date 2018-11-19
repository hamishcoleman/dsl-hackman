all: test

# Packages to install if we are running on Debian Stretch
PACKAGES_STRETCH := \
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
    python3-django-cors-headers \
    python3-django-oauth-toolkit \
    python3-django-redis \
    redis-server \
    gunicorn3 \
    python3-gevent \
    flake8 \

# Packages to install if we are running on Debian Unstable
PACKAGES_SID := $(PACKAGES_STRETCH) \
    python3-django-ratelimit \

# TODO - from the requirements.txt
# pyserial>=3.2.1
# RPi.GPIO>=0.6.3


build-depends:
	sudo apt-get install -y $(PACKAGES_SID)

build-depends-stretch:
	sudo apt-get install -y $(PACKAGES_STRETCH)

# Create or update the database
dev.db:
	python3 manage.py migrate

# Run the site with a development server
dev.run:
	python3 manage.py runserver

test.style:
	flake8

# Try to automatically detect if we are running on Debian or Ubuntu in the
# Travis-CI (because the ubnuts seem to have a different name for pytest. FFS)
PYTEST := /usr/bin/pytest-3
ifeq (,$(wildcard $(PYTEST)))
    PYTEST := /usr/bin/py.test-3
endif

test.unit:
	env DJANGO_SETTINGS_MODULE=hackman.settings_test $(PYTEST) --cov-report=term-missing --cov-fail-under=78 --cov=.

test: test.style test.unit
