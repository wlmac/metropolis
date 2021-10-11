setup: requirements.txt
	pg_config --version || (echo "libpq is required"; exit 1)
	python3 -m pip install -r requirements.txt
