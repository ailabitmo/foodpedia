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

    docker run -it --rm --name home_builder -v $POM_DIRECTORY_PATH:/usr/src/mymaven -w /usr/src/mymaven maven:3.2-jdk-7 mvn clean install -P $profile_name
    cp $POM_DIRECTORY_PATH/target/foodpedia-home-1.0-SNAPSHOT.war $POM_DIRECTORY_PATH/$RESULT_WAR_NAME

