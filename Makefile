.PHONY: help up down build test lint clean logs

help:
	@echo "Available commands:"
	@echo "  make up      - Start all services"
	@echo "  make down    - Stop all services"
	@echo "  make build   - Build Docker images"
	@echo "  make test    - Run pytest"
	@echo "  make lint    - Run flake8"
	@echo "  make clean   - Remove containers and volumes"
	@echo "  make logs    - Follow service logs"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

test:
	pytest tests/ -v --tb=short

lint:
	flake8 app/ tests/ --max-line-length=100

clean:
	docker-compose down -v --remove-orphans

logs:
	docker-compose logs -f