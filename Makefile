runserver:
	python manage.py runserver
test:
	python manage.py test
test-actions:
	python manage.py test movies.tests.test_actions
test-with-coverage:
	python -m coverage run --omit='*/migrations/*' manage.py test
coverage:
	coverage html