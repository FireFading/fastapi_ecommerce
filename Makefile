build:
	docker compose up --build

up:
	docker compose up

down:
	docker compose down && docker network prune --force

clean:
	docker stop $(docker ps -qa) && docker volume rm $(docker volume ls)
