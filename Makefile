install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

test:
	python -m pytest -vv tests/test_*.py

lint:
	pylint --disable=R,C *.py

all: install test format lint