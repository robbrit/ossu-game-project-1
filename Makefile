lint:
	pylint --rcfile=pylint.toml engine game

mypy:
	mypy main.py

test:
	python -m unittest

all_tests:
	$(MAKE) lint
	$(MAKE) mypy
	$(MAKE) test
