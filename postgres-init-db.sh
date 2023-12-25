#!/usr/bin/env bash

set -eu

echo '=== SETUP DATABASE'

echo '--- setting up users'

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" << EOF
CREATE USER metropolisuser WITH PASSWORD 'changeme_metropolis_password';
ALTER ROLE metropolisuser SET client_encoding TO 'utf8';
ALTER ROLE metropolisuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE metropolisuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE metropolis TO metropolisuser;
\c metropolis
GRANT ALL ON SCHEMA public TO metropolisuser;
EOF

cat ./pg_dump.sql.gz | gzip -d | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"
