#!/bin/bash

if [ "$1" = "-u" ]
then
  echo "run unittests"
  python -m unittest discover -s ./goodsmatrix/test/ -t ./goodsmatrix
else
  echo "run parser for the category $1"
  python -m goodsmatrix.main $1 /upload/dump.ttl
fi
