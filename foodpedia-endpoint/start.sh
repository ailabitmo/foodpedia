#!/bin/sh

# start the virtuoso service
echo "starting virtuoso …"
service virtuoso-opensource-6.1 start

echo "allow Cross-Origin Resource Sharing for /sparql"
isql-vt 1111 dba dba ./allow_cors_4_sparql.sql

# start the php5-fpm service
echo "starting php …"
service php5-fpm start

# start the nginx service
echo "starting nginx …"
service nginx start

echo "OntoWiki is ready to set sail!"
cat /ow-docker.fig

echo ""
echo "following log:"
OWLOG="/var/www/logs/ontowiki.log"
touch $OWLOG
chmod a+w $OWLOG
tail -f $OWLOG
