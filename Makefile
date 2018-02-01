.PHONY: default
default: init test lint

init:
	pip install -r requirements.txt

migrations:
	python manage.py makemigrations

test:
	python manage.py test

coverage:
	coverage run manage.py test

coverage_html: coverage
	coverage html

lint:
	flake8 .
