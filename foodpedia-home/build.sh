#!/bin/bash

if [ -z "$1" ]
then
  profile_name=development
  echo "a name of maven profile (development|testing|production) is not specified as command line argument.">&2
  echo "Use default $profile_name">&2
else
  profile_name=$1
fi

POM_DIRECTORY_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
RESULT_WAR_NAME=foodpedia-home-$profile_name.war

rm -f $POM_DIRECTORY_PATH/*.war
if [ -z "$M2_REPO" ]
then
    docker run --rm --name home_builder -v $POM_DIRECTORY_PATH:/usr/src/mymaven -w /usr/src/mymaven maven:3.2-jdk-7 mvn clean package -P $profile_name
else
    docker run --rm --name home_builder -v $POM_DIRECTORY_PATH:/usr/src/mymaven -v $M2_REPO:/root/.m2/repository/ -w /usr/src/mymaven maven:3.2-jdk-7 mvn clean package -P $profile_name
fi
mv $POM_DIRECTORY_PATH/target/foodpedia-home-1.0-SNAPSHOT.war $POM_DIRECTORY_PATH/$RESULT_WAR_NAME
rm -rf $POM_DIRECTORY_PATH/target
