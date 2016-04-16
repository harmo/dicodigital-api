FROM python:3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements/base.txt
ENV DJANGO_SETTINGS_MODULE dicodigital.settings
ENV DATABASE_URL sqlite:////usr/src/app/dicodigital.db
RUN python /usr/src/app/manage.py migrate && python /usr/src/app/manage.py createsuperuser && python /usr/src/app/manage.py loaddata fixtures/users.json fixtures/words.json fixtures/definitions.json && python /usr/src/app/manage.py collectstatic --noinput
EXPOSE 8000
CMD ["python", "/usr/src/app/manage.py", "runserver", "0.0.0.0:8000"]
