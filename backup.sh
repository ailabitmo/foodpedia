#!/bin/bash

FTP_SERVER_IP=192.168.134.9
BACKUP_NAME=foodpedia.tar.gz
BACKUP_FOLDER=/var/lib/virtuoso-opensource-6.1/db/backup

tar -czpvf $BACKUP_NAME $BACKUP_FOLDER

curl -T $BACKUP_NAME ftp://$FTP_SERVER_IP --user user:kExKt2ZC

rm $BACKUP_NAME
