FROM aksw/ontowiki-ubuntu-nginx

ADD virtuoso.ini /etc/virtuoso-opensource-6.1/virtuoso.ini
RUN mkdir -p /upload
ADD upload_dump.sh ./upload_dump.sh
RUN chmod +x ./upload_dump.sh
VOLUME /upload

ADD allow_cors_4_sparql.sql ./allow_cors_4_sparql.sql
ADD start.sh ./start.sh

ADD backup.sh ./backup.sh
RUN chmod +x ./backup.sh
