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

  echo "run parser for the category $1"
  echo "save results to $destination_filname"
  python -m goodsmatrix.main -p $1 $destination_filname
fi
