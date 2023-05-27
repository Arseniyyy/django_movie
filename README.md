# Django Movie

## Run with Docker

Run:
```
sh build.sh
```
Then:
```
docker compose up
```

## Testing

```
make test
```

This will run tests in both users and movies folders.

### How to run with the `coverage` package?

```
make test-coverage
```

Then run:

```
make coverage
```

ssh -i PEM_FILE.pem ubuntu@18.207.212.188
scp -i ~/django-movie/PEM_FILE.pem <file> ubuntu@18.207.212.188:<file>

### Remove all used containers
docker rm -f $(docker ps -a -q)

