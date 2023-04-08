makemigrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
runserver:
	python manage.py runserver
test:
	python manage.py test
test-movie-api:
	python manage.py test movies.tests.test_movie_api
test-actions:
	python manage.py test movies.tests.test_actions
test-permissions:
	python manage.py test movies.tests.test_permissions
test-views:
	python manage.py test movies.tests.test_views
test-custom-user-manager:
	python manage.py test users.tests.test_custom_user_manager
test-with-coverage:
	python -m coverage run --omit='*/migrations/*' manage.py test
coverage:
	coverage html