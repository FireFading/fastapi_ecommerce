## features
- JWT-authentication
- update profile with phone or name/ new email/phone/name, in registration user has only email and password, then can extend profile
- delete profile
- create/delete product if user is authenticated
- get products with or without filters and ordering
- rate product with from 1 to 5 stars
- get all ratings/avg rating for product
- delete rating
- get all ratings from users for product
- all features tested with pytest

[Screencast from 2023-04-13 17-40-30.webm](https://user-images.githubusercontent.com/91421235/231795625-8d372fca-0d53-4d7a-b111-e41dfe8e8395.webm)

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
