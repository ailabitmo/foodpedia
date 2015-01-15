FROM tomcat:7.0
RUN rm -rf $CATALINA_HOME/webapps/*

ADD webapps/ $CATALINA_HOME/webapps/

ADD form_configfile.sh /usr/local/form_configfile.sh
ADD run_pubby_on_tomcat.sh /usr/local/run_pubby_on_tomcat.sh
RUN ["chmod", "+x", "/usr/local/run_pubby_on_tomcat.sh"]

ENTRYPOINT ["sh", "/usr/local/run_pubby_on_tomcat.sh"]
CMD ["http://locahost:8080"]
