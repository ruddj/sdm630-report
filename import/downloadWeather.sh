#!/bin/bash

# Download weather data file for PVOutput upload
CONFIG=/etc/sdm630.conf

# Read config values from ini file
WUOUT=`awk -F ':' '{if (! ($0 ~ /^;/) && $0 ~ /WeatherFile/) print $2}' ${CONFIG} | tr -d ' '`
PWS=`awk -F ':' '{if (! ($0 ~ /^;/) && $0 ~ /PWS/) print $2}' ${CONFIG} | tr -d ' '`
WUAPI=`awk -F ':' '{if (! ($0 ~ /^;/) && $0 ~ /WUAPI/) print $2}' ${CONFIG} | tr -d ' '`

URL=http://api.wunderground.com/api/${WUAPI}/conditions/q/pws:${PWS}.json

/usr/bin/wget -q ${URL} -O ${WUOUT}

