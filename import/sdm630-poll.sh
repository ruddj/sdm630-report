#!/bin/bash

SDM630=/opt/sdm630/sdm630
DATADIR=/var/tmp
LATESTDATA=ACTsdm630.txt
RUNMAX=10  # Attempt this many times
SLEEP=18s  # wait this long between attempts

# Label file based on date-time
NOW=$(date +"%F-%H-%M")

DATAFILE=$DATADIR/ACT-$NOW.sdm
LOGFILE=$DATADIR/sdm-poll-$NOW.log

RUNCOUNT=0
EXIT=1

while [ $EXIT -ne 0 ] && [ $RUNCOUNT -lt $RUNMAX ]; do
	# Loop
	$SDM630 > $DATAFILE
	EXIT=$?
	
	let RUNCOUNT=RUNCOUNT+1 
	echo "$(date -I'seconds') Ran counter $RUNCOUNT times, $EXIT code" >> $LOGFILE
	if [ $EXIT -eq 0 ] ; then
		/bin/grep -Fq SUCCESS $DATAFILE
		EXIT=$?
	fi
	if [ $EXIT -ne 0 ] ; then
		/bin/rm $DATAFILE
		/bin/sleep $SLEEP
	fi
done

if [ $EXIT -eq 0 ] ; then
	#/bin/rm $DATADIR/$LATESTDATA
	/bin/cp $DATAFILE $DATADIR/$LATESTDATA
	#echo "$(date -I'seconds') SDM Ran correctly after $RUNCOUNT times and exited with $EXIT code" >> $LOGFILE
	/bin/rm $LOGFILE

else
	/bin/rm -f $DATAFILE
	echo "$(date -I'seconds') SDM Failed to run $RUNCOUNT times and exited with $EXIT code" | tee -a $LOGFILE
fi
