install:
	pip install -r requirements/dev.txt
install-sync:
	pip-sync requirements/dev.txt
compile-requirements:
	pip-compile requirements/base.in & pip-compile requirements/dev.in & pip-compile requirements/prod.in
build:
	docker compose build
start:
	docker compose up -d
stop:
	docker compose down
restart:
	docker compose down && docker compose build && docker compose up -d
migrate:
	docker compose exec web python manage.py migrate
makemigrations:
	docker compose exec web python manage.py makemigrations
createsuperuser:
	docker compose exec web python manage.py createsuperuser
lint:
	black .
.PHONY: docs
docs:
	-rm -rf docs/api.yaml
	-python manage.py generate_swagger -f yaml docs/api.yaml
