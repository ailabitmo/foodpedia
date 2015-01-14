FROM aksw/ontowiki-ubuntu-nginx

#ADD dump.ttl /usr/share/virtuoso-opensource-6.1/vad/dump.ttl
ADD upload_dump.sql ./upload_dump.sql
ADD upload_dump.sh ./upload_dump.sh
RUN chmod +x ./upload_dump.sh

ADD allow_cors_4_sparql.sql ./allow_cors_4_sparql.sql
ADD start.sh ./start.sh
