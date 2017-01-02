#!/bin/bash
set -e

source /venv/bin/activate
cd /usr/src/app/

if [ -e '.env' ]; then
    source .env
fi

DIRECT_MANAGE_COMMANDS=(
    'createsuperuser'
    'help'
    'migrate'
    'makemigrations'
    'runserver'
    'loaddata'
)

if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=secret
fi
if [ -z "$DJANGO_SETTINGS_MODULE" ]; then
    export DJANGO_SETTINGS_MODULE=dicodigital.settings
fi
if [ -z "$DEBUG" ]; then
    export DEBUG=True
fi

for COMMAND in ${DIRECT_MANAGE_COMMANDS[@]}; do
    if [[ $COMMAND == $1 ]]; then
        python manage.py $*
        exit
    fi
done
case $1 in
    tests)
        export DJANGO_SETTINGS_MODULE=tests.settings
        export DATABASE_URL=sqlite:///:memory:
        pytest -s
        ;;

    watch-tests)
        shift
        export DJANGO_SETTINGS_MODULE=tests.settings
        export DATABASE_URL=sqlite:///:memory:
        pytest -s $*
        watchmedo shell-command \
            --patterns="*.py" \
            --recursive \
            --command="pytest -s $*" \
            --drop \
            ./
        ;;

    install-fixtures)
        python manage.py loaddata fixtures/users.json 
        python manage.py loaddata fixtures/words.json
        python manage.py loaddata fixtures/definitions.json
        ;;

    *)
        $*
        ;;
esac