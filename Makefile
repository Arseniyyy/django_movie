PYTHON := python
MANAGE := $(PYTHON) manage.py

.PHONY: makemigrations migrate runserver test test-rating-model test-movie-api test-actor-api test-user-api test-movies-actions test-movies-permissions test-movies-views test-movies-serializers test-custom-user-manager test-coverage coverage

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate $(ARGS)

runserver:
	$(MANAGE) runserver 0.0.0.0:8000

test:
	$(MANAGE) test

test-refresh-jwt-token-for-user:
	$(MANAGE) test users.tests.test_user_api.UserAPITest.test_refresh_jwt_token_for_user

test-user-api:
	$(MANAGE) test users.tests.test_user_api

test-movies-actions:
	$(MANAGE) test movies.tests.test_actions

test-rating-model:
	$(MANAGE) test movies.tests.test_rating_model

test-movie-api:
	$(MANAGE) test movies.tests.test_movie_api

test-actor-api:
	$(MANAGE) test movies.tests.test_actor_api

test-genre-api:
	$(MANAGE) test movies.tests.test_genre_api

test-movies-permissions:
	$(MANAGE) test movies.tests.test_permissions

test-movies-views:
	$(MANAGE) test movies.tests.test_views

test-movies-serializers:
	$(MANAGE) test movies.tests.serializers.test_serializers

test-custom-user-manager:
	$(MANAGE) test users.tests.test_custom_user_manager

test-coverage:
	$(PYTHON) -m coverage run --omit='*/migrations/*' manage.py test

coverage:
	coverage html
