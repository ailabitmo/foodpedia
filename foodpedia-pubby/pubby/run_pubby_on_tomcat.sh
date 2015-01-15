#!/bin/bash

if [ -z "$1" ]
then
  echo "url of project's webbase is not specified as command line argument">&2
  exit 1
fi

if [ -z "$2" ]
then
  if [ -z "$ENDPOINT_PORT_8890_TCP_ADDR" ]
  then
    sparql_endpoint_url="http://foodpedia.tk/sparql"
    echo "A container with an alias 'endopoint' is not linked. Use the '$sparql_endpoint_url' as endpoint's url">&2
  else
    sparql_endpoint_url="http://endpoint:8890/sparql"
  fi
else
  sparql_endpoint_url=$2
fi

chmod +x /usr/local/form_configfile.sh
/bin/bash /usr/local/form_configfile.sh "$1" "$sparql_endpoint_url"
catalina.sh run
