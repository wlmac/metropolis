all: metropolis/local_rsa_privkey.pem metropolis/local_settings.py requirements.txt

.PHONY: all

metropolis/local_rsa_privkey.pem:
	openssl genrsa -out $@ 4096

metropolis/local_settings.py:
	cp metropolis/local_settings_sample.py metropolis/local_settings.py

requirements.txt: poetry.lock
	poetry run pip freeze -> $@ --exclude metroplis

