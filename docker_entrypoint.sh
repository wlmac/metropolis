#!/usr/bin/env bash

echo '=== INJECT'
for file in $(find /app-inject -type f); do
	dest="/app/${file#"/app-inject/"}"
	echo "--- inject $dest"
	cp "$file" "$dest"
	chown app:app "$dest"
	chmod u+rX "$dest"
done

case "$1" in
	gunicorn)
		cd /app/
		if [[ "$METROPOLIS_AUTOSETUP" == "yes" ]]; then
			echo '=== AUTOSETUP'
			echo '--- PUBLIC'
			chmod -R a+rwX /app-public
			echo '--- MIGRATE'
			runuser -u app -- /app/.venv/bin/python3 manage.py makemigrations # sometimes a package like oauth2_provider needs this
			runuser -u app -- /app/.venv/bin/python3 manage.py migrate
			echo '--- COLLECTSTATIC'
			runuser -u app -- /app/.venv/bin/python3 manage.py collectstatic --noinput
		fi
		runuser -u app -- /app/.venv/bin/gunicorn \
			--bind :28780 \
			--error-logfile - \
			metropolis.wsgi:application
	;;
	celery)
		shift
		runuser -u app -- /app/.venv/bin/celery -A metropolis worker --loglevel=INFO "$@"
	;;
	as-app)
		shift
		runuser -u app -- "$@"
	;;
	*)
		echo "unknown command $@"
		exit 1
	;;
esac
