PYTHON = python3
MAIN = a_maze_ing.py

install:
	pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN) config.txt

debug:
	$(PYTHON) -m pdb $(MAIN) config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf *.pyc

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict