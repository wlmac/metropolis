all: metropolis/local_rsa_privkey.pem metropolis/local_settings.py requirements.txt

.PHONY: all

metropolis/local_rsa_privkey.pem:
	openssl genrsa -out $@ 4096

metropolis/local_settings.py:
	cp metropolis/local_settings_sample.py metropolis/local_settings.py

requirements.txt: poetry.lock
	poetry export --without-hashes --format=requirements.txt > $@

sync-ruff-version:
	@command -v poetry >/dev/null 2>&1 || { \
		echo "poetry not found, skipping sync"; \
		exit 0; \
	}; \
	RUFF_VERSION=$$(awk '$$0 ~ /astral-sh\/ruff-pre-commit/ {found=1} found && $$1=="rev:" {gsub(/^v/, "", $$2); print $$2; exit}' .pre-commit-config.yaml | tr -d '\r'); \
	if [ -z "$$RUFF_VERSION" ]; then \
		echo "could not find ruff version in .pre-commit-config.yaml"; \
		exit 0; \
	fi; \
	CURRENT=$$(poetry run python -c "import importlib.metadata as m; print(m.version('ruff'))" 2>/dev/null | tr -d '\r'); \
	if [ "$$CURRENT" == "$$RUFF_VERSION" ]; then \
		echo "ruff version already matches: nothing to do, exiting..."; \
		exit 0; \
	fi; \
	poetry add --group dev ruff==$$RUFF_VERSION >/dev/null; \
	echo "Poetry synced to ruff==$$RUFF_VERSION"; echo "Please stage the changes and re-run commit."; \
	exit 1;

test:
	cd tests && docker compose up --build

.PHONY: test
