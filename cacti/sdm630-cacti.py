#!/usr/bin/python3

# Read in SDM630 values and output as single line for cacti


import datetime
import os.path
import sys
import configparser
import json
import argparse
__author__ = 'James Rudd'

APIKEY = ""
SYSTEMID = ""
EXTENDED = True
VERBOSE = 0

# Arguments
parser = argparse.ArgumentParser(description='Script to output SDM630 data for Cacti')
parser.add_argument('-v', '--verbose', help='Verbose Level', action='count')
parser.add_argument('-t', '--test',help='Test Data. Do not submit to PVOutput', action='store_true')
parser.add_argument('datafile', help = "Datafile that contains SDM630 readings")

args = parser.parse_args()

if args.verbose:
    VERBOSE = args.verbose

if args.test:
    SUBMIT = not args.test

if args.datafile:
    DATA = args.datafile
else:
    if VERBOSE > 0:
        print ('No datafile given')
    sys.exit(0)


if VERBOSE > 1:
    print("Config sections: "  )
    for section_name in config.sections():
        print ('Section:', section_name)
        print ('  Options:', config.options(section_name))
        for name, value in config.items(section_name):
            print ('  %s = %s' % (name, value))
        print

# Check data file exists
if not os.path.isfile(DATA):
    print (DATA + ' is missing')
    sys.exit(DATA + " does not exist.")


dataFilePath = DATA

if VERBOSE > 0:
    print ("Opening file: " + dataFilePath)
        
# Open data file
sdmdata = configparser.ConfigParser()

try:
    sdmdata.read(dataFilePath)
        
except OSError:
    print("Could not open " + dataFilePath)
    sys.exit("Could not open " + dataFilePath)

if sdmdata.get('MODBUS','read') != 'SUCCESSFUL' :
    print("SDM Data " + dataFilePath + " is invalid")
    sys.exit("SDM Data " + dataFilePath + " is invalid")

# Read Values Needed

# Watt Hours, Cumulative energy usage
# Multiply by 1000 as in kW
dEnergyCon = round( sdmdata.getfloat('MODBUS','IMPO_WH') * 1000)
dEnergyProd = round( sdmdata.getfloat('MODBUS','EXPO_WH') * 1000)

cactiData = {
    'L1_Volt' : round( sdmdata.getfloat('MODBUS','L1_Volt'), 2 ),
    'L2_Volt' : round( sdmdata.getfloat('MODBUS','L2_Volt'), 2 ),
    'L3_Volt' : round( sdmdata.getfloat('MODBUS','L3_Volt'), 2 ),
    'Avg_Volt' : round( sdmdata.getfloat('MODBUS','Avg_Volt'), 2 ),
    'L1_Amps' : round( sdmdata.getfloat('MODBUS','L1_Amps'), 2 ),
    'L2_Amps' : round( sdmdata.getfloat('MODBUS','L2_Amps'), 2 ),
    'L3_Amps' : round( sdmdata.getfloat('MODBUS','L3_Amps'), 2 ),
    'TOT_Amp' : round( sdmdata.getfloat('MODBUS','TOT_Amp'), 2 ),
    'L1_Watt' : int(round( sdmdata.getfloat('MODBUS','L1_Watt'), 0 )),
    'L2_Watt' : int(round( sdmdata.getfloat('MODBUS','L2_Watt'), 0 )),
    'L3_Watt' : int(round( sdmdata.getfloat('MODBUS','L3_Watt'), 0 )),
    'P_TOT_W' : int(round( sdmdata.getfloat('MODBUS','P_TOT_W'), 0 )),
    'L1_PF' : round( sdmdata.getfloat('MODBUS','L1_PF') * 100, 2 ),
    'L2_PF' : round( sdmdata.getfloat('MODBUS','L2_PF') * 100, 2 ),
    'L3_PF' : round( sdmdata.getfloat('MODBUS','L3_PF') * 100, 2 ),
    'P_FACTO' : round( sdmdata.getfloat('MODBUS','P_FACTO') * 100, 2 ),
    'Freq' : round( sdmdata.getfloat('MODBUS','Freq'), 2 ),
    'IMPO_WH' : dEnergyCon,
    'EXPO_WH' : dEnergyProd,
}


if VERBOSE > 0:
    print (repr(cactiData) )

for x in cactiData:
    print (x + ':' + str(cactiData[x]) + ' ', end="")

print("")
