#!/bin/bash

if [ "$1" = "-u" ]
then
  echo "run unittests"
  python -m unittest discover -s ./goodsmatrix/test/ -t ./goodsmatrix
else
  if [ -z "$2" ]
  then
      destination_filname=/upload/dump.ttl
  else
      destination_filname=$2
  fi

  if [ -z "$agrovoc_endpoint" ]
  then
      agrovoc_endpoint=http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc
  fi

  echo "run parser for the category $1"
  echo "save results to $destination_filname"
  if [ -z "$yandexapikey" ]
  then
      echo "without translation. Set the env variable yandexapikey to translate results"
      python -m goodsmatrix.main -p -a $agrovoc_endpoint $1 $destination_filname
  else
      echo "translate results"
      python -m goodsmatrix.main -p -a $agrovoc_endpoint -k $yandexapikey $1 $destination_filname
  fi
fi
