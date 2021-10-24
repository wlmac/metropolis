git-setup:
	cp -i scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

pre-commit: fmt-check;

fmt:
	python3 -m black .
	git diff --name-only --cached | xargs python3 -m isort .

fmt-check:
	python3 -m black --check .
	git diff --name-only --cached | xargs -P 32 python3 -m isort --check

fmt-setup:
	python3 -m pip install black isort

.PHONY: setup-git pre-commit fmt fmt-check fmt-setup;
