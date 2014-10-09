#!/bin/bash

#mkdir /tmp/WEB-INF
#cp /etc/jenkins/init.groovy /tmp/WEB-INF/init.groovy
#cd /tmp && zip -g /usr/share/jenkins/jenkins.war WEB-INF/init.groovy

exec java -jar /usr/share/jenkins/jenkins.war --prefix=/
