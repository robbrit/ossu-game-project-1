lint:
	pylint --rcfile=pylint.toml engine game

mypy:
	mypy main.py game/**/*.py engine/builtin.py

test:
	python -m unittest -v

cov:
	coverage run -m unittest -v
	coverage html
	open htmlcov/index.html

all_tests:
	$(MAKE) lint
	$(MAKE) mypy
	$(MAKE) test
