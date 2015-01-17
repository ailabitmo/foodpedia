#!/bin/bash

if [ -z "$1" ]
then
  echo "url of project's webbase is not specified as command line argument">&2
  exit 1
else
  homeURL=$1
fi

if [ -z "$2" ]
then
  if [ -z "$ENDPOINT_PORT_8890_TCP_ADDR" ]
  then
    sparqlEndpointURL="http://foodpedia.tk/sparql"
    echo "A container with an alias 'endopoint' is not linked. Use the '$sparqlEndpointURL' as endpoint's url">&2
  else
    sparqlEndpointURL="http://endpoint:8890/sparql"
  fi
else
  sparqlEndpointURL=$2
fi
export homeURL sparqlEndpointURL

WEBAPP_HOME=/usr/local/tomcat/webapps/ROOT/WEB-INF
envsubst <$WEBAPP_HOME/config.ttl | sponge $WEBAPP_HOME/config.ttl
envsubst <$WEBAPP_HOME/prefixes.n3 | sponge $WEBAPP_HOME/prefixes.n3

catalina.sh run
