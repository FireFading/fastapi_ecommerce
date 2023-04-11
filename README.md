## features
- JWT-authentication
- update profile with phone or name/ new email/phone/name, in registration user has only email and password, then can extend profile
- create product if user is authenticated
- get products with or without filters and ordering
- rate product with from 1 to 5 stars
- get all ratings from users for product
- all features tested with pytest

## setup
- in env.example all variables used in project, change it to .env, several variables that are common, already define as example, secret variables is empty
add to .env

## run project
- `docker compose up --build` OR `make up`

## down docker
- `docker compose down && docker network prune --force` OR `make down`

## database
- connect to postgres: `docker exec -it postgres psql -U postgres`

## migrations
- connect to docker container: `docker exec -it fastapi bash`
- apply migrations: `alembic upgrade head` in fastapi container
- create new migrations: `alembic revision --autogenerate -m "<migration name>"` in fastapi container

## formatting and linting
- run ufmt: `ufmt format .`
- run black: `black --config=configs/.black.toml app`
- run ruff: `ruff check --config=configs/.ruff.toml --fix app`
- run flake8: `flake8 --config=configs/.flake8 app`

- OR `nox` in root

## run tests
- `pytest .` OR `pytest ./tests` OR run `nox`
