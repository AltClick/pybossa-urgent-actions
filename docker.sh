#!/bin/bash

virtualenv -p python venv
currentDir=`pwd`
virtualenvPath='venv/bin/activate'
source $currentDir/$virtualenvPath

bash db_create.sh
2>/dev/null 1>&2 bash rqscheduler.sh &
2>/dev/null 1>&2 bash jobs.sh &

/usr/sbin/apache2ctl -D FOREGROUND
