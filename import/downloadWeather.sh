#!/bin/bash

# Download weather data file for PVOutput upload
CONFIG=/etc/sdm630.conf
_V=1

# Read config values from ini file
WUOUT=`awk -F ':' '{if (! ($0 ~ /^;/) && $0 ~ /WeatherFile/) print $2}' ${CONFIG} | tr -d ' '`
PWS=`awk -F ':' '{if (! ($0 ~ /^;/) && $0 ~ /PWS/) print $2}' ${CONFIG} | tr -d ' '`
WUAPI=`awk -F ':' '{if (! ($0 ~ /^;/) && $0 ~ /WUAPI/) print $2}' ${CONFIG} | tr -d ' '`

URL=http://api.wunderground.com/api/${WUAPI}/conditions/q/pws:${PWS}.json

/usr/bin/wget -q ${URL} -O ${WUOUT}.${PWS}

# Test download was succesful
/bin/grep -Fq current_observation "${WUOUT}.${PWS}"
EXIT=$?

if [[ $EXIT -eq 0 ]] ; then
	/bin/cp "${WUOUT}.${PWS}" ${WUOUT}
else
	if [[ $_V -ge 1 ]] ; then
		echo "Weather download Failed"
		cat "${WUOUT}.${PWS}"
	fi
		# Failed Weather Download
fi
