SHELL := /bin/bash

dev:
	docker compose up --build

deploy:
	docker login
	docker build -t nicolldouglas/freemium:latest .
	docker push nicolldouglas/freemium:latest