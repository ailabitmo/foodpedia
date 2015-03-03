FROM debian
ENV CATALINA_HOME /usr/local/tomcat

RUN apt-get update && apt-get install -y \
    unzip
ADD http://wifo5-03.informatik.uni-mannheim.de/pubby/download/pubby-0.3.3.zip /usr/local/src/pubby-0.3.3.zip
RUN unzip -o /usr/local/src/pubby-0.3.3.zip -d /tmp/
#RUN rm -rf $CATALINA_HOME/webapps/*
RUN mkdir -p $CATALINA_HOME/webapps
RUN mv /tmp/pubby-0.3.3/webapp $CATALINA_HOME/webapps/ROOT

ADD prefixes.n3 $CATALINA_HOME/webapps/ROOT/WEB-INF/prefixes.n3
ADD config.ttl $CATALINA_HOME/webapps/ROOT/WEB-INF/config.ttl
ADD footer.vm $CATALINA_HOME/webapps/ROOT/WEB-INF/templates/footer.vm
ADD header.vm $CATALINA_HOME/webapps/ROOT/WEB-INF/templates/header.vm

VOLUME ["/usr/local/tomcat/webapps/"]
