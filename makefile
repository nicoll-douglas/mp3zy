ENV_NAME = pythonenv

python-env:
	python3 -m venv $(ENV_NAME) && bash -c "source ./$(ENV_NAME)/bin/activate && exec bash"

run:
	./$(ENV_NAME)/bin/python main.py

install-deps:
	./$(ENV_NAME)/bin/pip install -r requirements.txt