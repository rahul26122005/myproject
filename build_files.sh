#!/bin/bash

# Example of using an environment variable to specify a path
export MY_PATH_ENV_VAR="C:\Users\rahul\.virtualenvs\django-B5393Xc0"

#!/bin/bash
apt-get update
apt-get install -y libmysqlclient-dev


# Use the environment variable in your script
pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate --settings=dj_project.settings

# Example: Use an environment variable to set the Django settings module
export DJANGO_SETTINGS_MODULE=myproject.settings.production

# Run any other commands needed for your deployment
