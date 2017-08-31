#!/usr/bin/python3

# Read in SDM630 values and send to PVOutput

# Crontab Command
# */5 *   *   *   *    /opt/sdm630/sdm630-poll.sh
# 1-59/5 *   *   *   *    /opt/sdm630/pvoutput.py

import datetime
import requests
import os.path
import sys
import configparser
import json
import argparse
__author__ = 'James Rudd'

PVAPIURL = "http://pvoutput.org/service/r2/addstatus.jsp"
CONFIG = "/etc/sdm630.conf"
APIKEY = ""
SYSTEMID = ""
EXTENDED = True
TEMPERATURE = True
DATADIR = "/var/tmp"
WUOUT = "/var/tmp/weather.json"
VERBOSE = 1
SUBMIT = True

# Arguments
parser = argparse.ArgumentParser(description='Script to upload consumption data to PVOutput')
parser.add_argument('-c', '--config', help = 'Configuration File')
parser.add_argument('-v', '--verbose', help='Verbose Level', action='count')
parser.add_argument('-t', '--test',help='Test Data. Do not submit to PVOutput', action='store_true')
args = parser.parse_args()

if args.verbose:
    VERBOSE = args.verbose

if args.config:
    CONFIG = args.config

if args.test:
    SUBMIT = not args.test


# Open config file
if not os.path.isfile(CONFIG):
    if VERBOSE > 0:
        print (CONFIG + ' is missing')
    sys.exit(CONFIG + " does not exist.")
    
config = configparser.ConfigParser()

try:
    if VERBOSE > 1:
        print("Loading config: " + CONFIG)
    config.read(CONFIG)
    
except OSError:
    if VERBOSE > 0:
        print("Could not open " + CONFIG)
    sys.exit("Could not open " + CONFIG)

try:
    APIKEY = config.get('PVOutput', 'PVAPI')
    SYSTEMID = config.get('PVOutput', 'SystemID')
except ConfigParser.NoOptionError:
    sys.exit("Missing PVOutput API or SystemID")

if config.has_option('PVOutput', 'PVextend'):
    EXTENDED = config.getboolean('PVOutput', 'PVextend', fallback=EXTENDED)
    
if config.has_option('PVOutput', 'DataDir'):
    DATADIR = config.get('PVOutput', 'DataDir', fallback=DATADIR)
    
if config.has_option('PVOutput', 'WeatherFile'):
    WUOUT = config.get('PVOutput', 'WeatherFile', fallback=WUOUT)

if VERBOSE > 1:
    print("Config sections: "  )
    for section_name in config.sections():
        print ('Section:', section_name)
        print ('  Options:', config.options(section_name))
        for name, value in config.items(section_name):
            print ('  %s = %s' % (name, value))
        print

# Check data file exists
if not os.path.isdir(DATADIR):
    print (DATADIR + ' is missing')
    sys.exit(DATADIR + " does not exist.")

for dataFile in os.listdir(DATADIR):
    if dataFile.endswith(".sdm"):
        dataFilePath = DATADIR + '/' + dataFile
        # Read file time
        strGenTime = os.path.getmtime(dataFilePath)
        genTime = datetime.datetime.fromtimestamp(strGenTime)

        dDate = genTime.strftime("%Y%m%d")
        dTime = genTime.strftime("%R")

        # Check date is modern in case NTP has not stablilesd.
        # Raspberry Pi has no Real Time Clock
        if datetime.date(2016, 1, 1) > genTime.date() :
            print ("Date has not been updated from NTP")
            os.remove(dataFilePath)
            continue

        if VERBOSE > 0:
            print ("Opening file: " + dataFilePath)
                
        # Open data file
        sdmdata = configparser.ConfigParser()

        try:
            sdmdata.read(dataFilePath)
                
        except OSError:
            print("Could not open " + dataFilePath)
            os.remove(dataFilePath)
            continue

        if sdmdata.get('MODBUS','read') != 'SUCCESSFUL' :
            print("SDM Data " + dataFilePath + " is invalid")
            # os.remove(dataFilePath)
            os.rename(dataFilePath, dataFilePath+'-old')
            continue

        # Read Values Needed

        # Watt Hours, Cumulative energy usage
        # Multiply by 1000 as in kW
        dEnergyCon = round( sdmdata.getfloat('MODBUS','IMPO_WH') * 1000)

        # Watts, instantaneous usage
        dPowerCon = round( sdmdata.getfloat('MODBUS','P_TOT_W') )

        # System Voltage
        dVoltage = round( sdmdata.getfloat('MODBUS','Avg_Volt'), 2 )

        # Get Temperature
        if TEMPERATURE:
            if os.path.isfile(WUOUT):
                strGenTime = os.path.getmtime(WUOUT)
                genTime = datetime.datetime.fromtimestamp(strGenTime)
                
                if genTime > datetime.datetime.now() - datetime.timedelta(hours=1) :
                    try:
                        with open(WUOUT) as data_file:
                            weather = json.load(data_file)
							dTemp = weather['current_observation']['temp_c'] 
                    except ValueError:
                        TEMPERATURE = False
                        if VERBOSE > 0:
                            print ("Failed reading weather from: " + WUOUT)
                else:
                    TEMPERATURE = False

                 
            else:
                TEMPERATURE = False


        # CURL Submit String
        pvHeaders = {
                'X-Pvoutput-Apikey': APIKEY,
                'X-Pvoutput-SystemId': SYSTEMID,
                 }

        pvData={'d': dDate,
                't': dTime,
                'v3': dEnergyCon,
                'v4': dPowerCon,
                'v6': dVoltage,
                'c1': 1,
                }
        
        if EXTENDED:
            dPowerConL1 = round( sdmdata.getfloat('MODBUS','L1_Watt'), 3 )
            dPowerConL2 = round( sdmdata.getfloat('MODBUS','L2_Watt'), 3 )
            dPowerConL3 = round( sdmdata.getfloat('MODBUS','L3_Watt'), 3 )
            pvData['v7'] = dPowerConL1
            pvData['v8'] = dPowerConL2
            pvData['v9'] = dPowerConL3

        if TEMPERATURE:
            pvData['v5'] = dTemp

        if VERBOSE > 0:
            print (repr(pvHeaders))
            print (repr(pvData) )

        if SUBMIT:
            r = requests.post(PVAPIURL, data=pvData, headers=pvHeaders)
            # Check return code is OK, and remove data file    
            if r.status_code == requests.codes.ok :
                os.remove(dataFilePath)
            else:
                print(r.status_code, r.reason)
                # Raise exception with details of failed connection
                r.raise_for_status()
			
        continue
    else:
        # Not an SDM file so go to next
        continue	
