all: metropolis/local_rsa_privkey.pem metropolis/local_settings.py requirements.txt

.PHONY: all

metropolis/local_rsa_privkey.pem:
	openssl genrsa -out $@ 4096

metropolis/local_settings.py:
	cp metropolis/local_settings_sample.py metropolis/local_settings.py

requirements.txt: poetry.lock
	poetry export --without-hashes --format=requirements.txt > $@

sync-ruff-version:
	@RUFF_VERSION=$$(awk '$$0 ~ /astral-sh\/ruff-pre-commit/ {found=1} found && $$1=="rev:" {gsub(/^v/, "", $$2); print $$2; exit}' .pre-commit-config.yaml | tr -d '\r'); \
	if [ -z "$$RUFF_VERSION" ]; then \
		echo "WARNING: Could not find ruff version or pre-commit hook in .pre-commit-config.yaml"; \
		exit 0; \
	fi; \
	echo "Found pre-commit ruff version: $$RUFF_VERSION"; \
	RUFF_POETRY_VERSION=$$(poetry show ruff --no-ansi 2>/dev/null | awk '$$1=="version" {print $$3}' | tr -d '\r'); \
	if [ -z "$$RUFF_POETRY_VERSION" ]; then \
		echo "Could not find ruff version in poetry"; \
		exit 0; \
	else \
		echo "Found poetry ruff version: $$RUFF_POETRY_VERSION"; \
	fi; \
	if [ "$$RUFF_VERSION" == "$$RUFF_POETRY_VERSION" ]; then \
		echo "Ruff versions match: nothing to do, exiting..."; \
		exit 0; \
	fi; \
	echo "Syncing ruff version in poetry"; \
	poetry add --group dev ruff==$$RUFF_VERSION >/dev/null; \
	echo "Ruff version updated in poetry to $$RUFF_VERSION"; echo "Please stage the changes and re-run commit."; \
	exit 1; \

test:
	cd tests && docker compose up --build

.PHONY: test
