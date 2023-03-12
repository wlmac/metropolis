#!/usr/bin/env nix-shell
#! nix-shell -i bash ./default.nix

set -eu
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m poetry run pip freeze > requirements.txt
./manage.py runserver
