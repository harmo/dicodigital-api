FROM django:onbuild
RUN pip install -r requirements/dev.txt
ENV DJANGO_SETTINGS_MODULE dicodigital.settings
ENV DATABASE_URL sqlite:////usr/src/app/dicodigital.db
ENV DEBUG True
WORKDIR /usr/src/app
RUN python manage.py migrate && python manage.py createsuperuser && python manage.py loaddata fixtures/users.json fixtures/words.json fixtures/definitions.json
ENTRYPOINT [ "python", "manage.py", "runserver_plus" ]
CMD [ "0.0.0.0:8000" ]
