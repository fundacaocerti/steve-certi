FROM nginx:1.25
RUN mkdir /webserver

COPY webserver-entrypoint.sh /webserver/webserver-entrypoint.sh
COPY nginx.conf.tmpl /webserver/nginx.conf.tmpl
COPY wait-for.sh /webserver/wait-for.sh
WORKDIR /webserver
RUN chmod +x webserver-entrypoint.sh

EXPOSE 80