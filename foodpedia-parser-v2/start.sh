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
      echo "Parse without translation. Set the env variable yandexapikey to translate results"
      if [ -z "$old_endpoint" ]
      then
          echo "Do not use previous results of parsing"
          echo "Set the env variable old_endpoint to use them"
          python -m goodsmatrix.main -p -a $agrovoc_endpoint $1 $destination_filname
      else
          echo "Parse only new items"
          echo "Merge results with $old_endpoint to get the whole dump"
          python -m goodsmatrix.main -p -a $agrovoc_endpoint -o $old_endpoint $1 $destination_filname
      fi
  else
      echo "Parse with translation of results"
      if [ -z "$old_endpoint" ]
      then
          echo "Do not use previous results of parsing"
          echo "Set the env variable old_endpoint to use them"
          python -m goodsmatrix.main -p -a $agrovoc_endpoint -k $yandexapikey $1 $destination_filname
      else
          echo "Parse only new items"
          echo "Merge results with $old_endpoint to get the whole dump"
          python -m goodsmatrix.main -p -a $agrovoc_endpoint -k $yandexapikey -o $old_endpoint $1 $destination_filname
      fi
  fi
fi
