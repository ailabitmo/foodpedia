FROM tomcat:7.0
# gettext for envsubst
# moreutils for sponge
RUN apt-get update && apt-get install -y \
  gettext \
  moreutils

RUN rm -rf $CATALINA_HOME/webapps/*
ADD webapps/ $CATALINA_HOME/webapps/

ADD run_pubby_on_tomcat.sh /usr/local/run_pubby_on_tomcat.sh
RUN ["chmod", "+x", "/usr/local/run_pubby_on_tomcat.sh"]

ENTRYPOINT ["sh", "/usr/local/run_pubby_on_tomcat.sh"]
CMD ["http://locahost:8080"]
