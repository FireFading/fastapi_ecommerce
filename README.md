## Features
- JWT-authentication
- update profile with phone or name/ new email/phone/name, in registration user has only email and password, then can extend profile
- activate profile with email verification
- delete profile
- create/delete product if user is authenticated
- get products with or without filters and ordering
- rate product with from 1 to 5 stars
- get all ratings/avg rating for product
- delete rating
- get all ratings from users for product
- get average rating for product
- all features tested with pytest

[Screencast from 2023-04-13 17-40-30.webm](https://user-images.githubusercontent.com/91421235/231795625-8d372fca-0d53-4d7a-b111-e41dfe8e8395.webm)

## Installation
- in env.example all variables used in project, change it to .env, several variables that are common, already define as example, secret variables is empty

## run project
```bash
  docker compose up --build
```
OR `make build` - first time
```bash
  docker compose up
```
OR `make up` - run without building, also you can prove -d flag to run as daemon

## Down docker
```bash
  docker compose down && docker network prune --force
```
OR `make down`

## Database
- connect to postgres
```bash
  docker exec -it postgres psql -U postgres
```

## Migrations
- run docker containers 
- connect to docker container
```bash
  docker exec -it fastapi bash
```
- apply migrations  in fastapi container
```bash
  alembic upgrade head
```
- create new migrations in fastapi container
```bash
  alembic revision --autogenerate -m "<migration name>"
``` 

## Formatting and linting
- run ufmt: `ufmt format .`
- run black: `black --config=configs/.black.toml app`
- run ruff: `ruff check --config=configs/.ruff.toml --fix app`
- run flake8: `flake8 --config=configs/.flake8 app`

- OR `nox` in root

## Testing
- `pytest .` OR `pytest ./tests` OR run `nox`
