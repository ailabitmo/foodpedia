# This image should be splited to 'builder' with JDK and 'main' image with tomcat
# But I don't want to complicate build procdure for this small service

FROM tomcat:7.0

RUN apt-get update && apt-get install -y \
  openjdk-7-jdk

WORKDIR /usr/src/
EXPOSE 8080

#http://serverfault.com/questions/658502/tomcat-8-hangs-on-startup-while-deploying-webapp-possibly-related-to-entropy-ge
ENV JAVA_OPTS=-Djava.security.egd=file:/dev/./urandom 
ENV WEBAPP_DIR=$CATALINA_HOME/webapps/ROOT

RUN rm -rf $CATALINA_HOME/webapps/*
ADD web/ $WEBAPP_DIR

#Why is 'foodpedia.itmo.ru' used instead of 'foodpedia.tk' ???
RUN mkdir -p $WEBAPP_DIR/WEB-INF/classes/ru/itmo/foodpedia
ADD src/ /usr/src/
RUN javac -cp $CATALINA_HOME/lib/servlet-api.jar -d $WEBAPP_DIR/WEB-INF/classes/ ./ru/itmo/foodpedia/FoodPedia.java
