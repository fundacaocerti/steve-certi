#! /bin/bash
# Nginx configuration files don't accept environment variables so we replace
# the templates using this command. This includes replacing ${DOLLAR} for '$'
export DOLLAR='$'
envsubst < /webserver/nginx.conf.tmpl > /etc/nginx/nginx.conf

# We wait for the frontend to become available before starting the reverse
# proxy
./wait-for.sh --host="$STEVE_HOST" --port="$STEVE_PORT" --timeout=300
nginx -g "daemon off;"