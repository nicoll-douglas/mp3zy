SHELL := /bin/bash

all: prod

dev:
	docker compose up --build

prod:
	docker compose up -d && docker logs freemium -f

pyvenv:
	python3 -m venv .pyvenv
	source .pyvenv/bin/activate
	pip install -r requirements.txt