git-setup:
	mv .git/hooks/pre-commit .git/hooks/pre-commit2
	printf "#!/bin/sh\n\nmake pre-commit" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

pre-commit: fmt-check;

# TODO(colourdelete): only run fmt on changed files

fmt-setup:
	python3 -m pip install --upgrade black isort

fmt:
	python3 -m black --version
	python3 -m black .
	python3 -m isort --version
	python3 -m isort .

fmt-check:
	python3 -m black --version
	python3 -m black --check .
	python3 -m isort --version
	python3 -m isort --check .

.PHONY: setup-git pre-commit fmt fmt-check fmt-setup;
