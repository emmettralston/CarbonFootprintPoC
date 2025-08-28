.PHONY: up down logs api db


up:
	docker compose up --build -d


down:
	docker compose down -v


logs:
	docker compose logs -f --tail=200


api:
	docker compose exec api bash


db:
	docker compose exec db psql -U $$POSTGRES_USER -d $$POSTGRES_DB
