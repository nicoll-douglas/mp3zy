SHELL := /bin/bash

all: prod

dev:
	docker compose up --build

prod:
	python3 main.py

pyvenv:
	python3 -m venv .pyvenv
	source .pyvenv/bin/activate