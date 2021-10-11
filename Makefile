setup: git-setup requirements.txt
	pg_config --version || (echo "libpq is required"; exit 1)
	python3 -m pip install -r requirements.txt

git-setup:
	mv .git/hooks/pre-commit .git/hooks/pre-commit2
	printf "#!/bin/sh\n\nmake pre-commit" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

pre-commit: fmt-check;

fmt:
	python3 -m black .
	python3 -m isort .

fmt-check:
	python3 -m black --check .
	git diff --name-only --cached | xargs -P 32 -r python3 -m isort --check

fmt-setup:
	python3 -m pip install black isort

.PHONY: setup-git pre-commit fmt fmt-check fmt-setup setup;
