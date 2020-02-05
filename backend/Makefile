all: run

run:
	env FLASK_APP=blog FLASK_ENV=development flask run

db-init:
	env FLASK_APP=blog flask db init

db-migrate:
	env FLASK_APP=blog flask db migrate

db-upgrade:
	env FLASK_APP=blog flask db upgrade

db-downgrade:
	env FLASK_APP=blog flask db downgrade

lint:
	flake8 blog/ --count --max-complexity=10 --config=.flake8
