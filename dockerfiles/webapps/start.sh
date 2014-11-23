#!/bin/bash

service tomcat7 restart
service nginx restart

tail -f -n 100 /var/log/tomcat7/catalina.out
