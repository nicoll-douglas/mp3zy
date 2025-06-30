SHELL := /bin/bash

all: pyvenv dev

dev:
	docker compose up --build

deploy:
	docker login
	docker build -t nicolldouglas/freemium:latest .
	docker push nicolldouglas/freemium:latest

pyvenv:
	python3 -m venv .pyvenv
	source .pyvenv/bin/activate
	pip install -r requirements.txt