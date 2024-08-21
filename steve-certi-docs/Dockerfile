
FROM swaggerapi/swagger-ui:v5.17.14
RUN mkdir steve
COPY swagger-server-configs/default.conf.template /etc/nginx/templates/default.conf.template
COPY steve-certi-openapi.yaml  /usr/share/nginx/html/docs/steve-certi-openapi.yaml
COPY steve-certi-openapi.yaml  /steve/steve-certi-openapi.yaml
ENV SWAGGER_JSON=/steve/steve-certi-openapi.yaml