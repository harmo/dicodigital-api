help:
	@echo "usage:"
	@echo "	help			display this message"
	@echo "	makemigrations	create new migrations"
	@echo "	migrations		run migrations"
	@echo "	createsuperuser	create a superuser"
	@echo "	build 			build the containers"
	@echo "	install 		install all the app"
	@echo "	up  			run app and dependancies"
	@echo "	down 			stop app and dependancies + remove containers"
	@echo "	shell			connect to container with bash shell"
	@echo "	shell-plus		run enhanced development shell"
	@echo "	unit-tests 			run unit tests "
	@echo "	watch-tests		also run unit tests whenever python files changed"
	

RUN=docker-compose run --rm
EXEC=docker-compose exec

makemigrations:
	$(RUN) web makemigrations

migrations:
	$(RUN) web migrate

createsuperuser:
	$(RUN) web createsuperuser

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

install: build up migrations
	echo "Done."

shell:
	$(EXEC) web /bin/bash

shell-plus:
	$(EXEC) web shell_plus

test:
	$(RUN) web tests

watch-test:
	$(RUN) web watch-tests

logs:
	docker-compose logs -f web 