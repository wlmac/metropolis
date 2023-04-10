#!/usr/bin/env bash

case "$1" in
	gunicorn)
		/app/.venv/bin/gunicorn \
			--bind :28780 \
			--error-logfile - \
			--config /app/container/gunicorn.py \
			metropolis.wsgi:application
	;;
	celery)
		runuser -u app -- celery -A metropolis worker --loglevel=INFO
	;;
	*)
		echo "unknown command $1"
		exit 1
	;;
esac
