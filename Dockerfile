FROM python:3.5

RUN apt-get update && apt-get install -y \
	sqlite3 \
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app

ADD ./requirements/ /usr/src/app/requirements

WORKDIR /
RUN python -m venv venv
RUN ./venv/bin/pip install --no-cache-dir -r /usr/src/app/requirements/dev.txt

ADD ./docker /usr/src/app/docker/
RUN chmod +x /usr/src/app/docker/docker-entrypoint.sh

ENTRYPOINT ["/usr/src/app/docker/docker-entrypoint.sh"]