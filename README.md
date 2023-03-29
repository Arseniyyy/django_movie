# Django Movie

## Run with Docker

You need to create .docker.env before starting the command below. `.docker.env` includes environmental data that Django needs to connect to the database.

```
docker run --rm --env-file ./.docker.env -p 5431:5432 -d postgres:15.1-alpine
```

You change the user to postgres after you connected:

```
docker exec -it [name-of-container] bash
psql -U postgres
```

Next, exit the postgres bash, cd to your project and run `python manage.py migrate`

Now you can change everything in the running container.
