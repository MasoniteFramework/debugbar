init:
	pip install .
test:
	python -m pytest tests
lint:
	python -m flake8 src/debugbar/ --ignore=E501,F401,E203,E128,E402,E731,F821,E712,W503,F811
format:
	black src/debugbar
	black tests/
	make lint
sort:
	isort tests
	isort src/debugbar
coverage:
	python -m pytest --cov-report term --cov-report xml --cov=src/debugbar tests/
	python -m coveralls
show:
	python -m pytest --cov-report term --cov-report html --cov=src/debugbar tests/
cov:
	python -m pytest --cov-report term --cov-report xml --cov=src/debugbar tests/
publish:
	pip install twine
	make test
	python setup.py sdist
	twine upload dist/*
	rm -fr build dist .egg debugbar.egg-info
	rm -rf dist/*
pub:
	python setup.py sdist
	twine upload dist/*
	rm -fr build dist .egg debugbar.egg-info
	rm -rf dist/*
pypirc:
	cp .pypirc ~/.pypirc