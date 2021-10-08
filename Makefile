setup-git:
	rm -f .git/hooks/pre-commit
	echo "make pre-commit" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

pre-commit: fmt-check;

fmt-check:
	black --version
	python3 -m black .
	isort --version
	python3 -m isort .

fmt:
	black --version
	python3 -m black --check .
	isort --version
	python3 -m isort --check .
	# TODO(colourdelete): add & format changed files

.PHONY: setup-git pre-commit fmt
