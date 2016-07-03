#!/usr/bin/python3

# Read in SDM630 values and return SNMP

import datetime
import os.path
import sys, getopt
import configparser
import argparse
__author__ = 'James Rudd'

DATA="/var/tmp/ACTsdm630.txt"
OidBase = ".1.3.6.1.4.1.12345.1.1"; 
VERBOSE = 1
Next = False

# Arguments
parser = argparse.ArgumentParser(description='Script to return consumption data to SNMP')
parser.add_argument('-v', '--verbose', help = 'Verbose Level. -vv = Very Verbose', action = 'count')
parser.add_argument('-i', '--input', help = 'Input consumption data file')
parser.add_argument('-s', '--set', help = 'SNMP Set (no action)')
parser.add_argument('-g', '--get', help = 'SNMP Get (Default)', action='store_true')
parser.add_argument('-n', '--next', help = 'SNMP GetNext - determine next valid instance', action='store_true')
parser.add_argument('OID', help = "SNMP OID to retrieve. Should begin with " + OidBase)

#print(parser.parse_args(['--help']))


args = parser.parse_args([OidBase + '.1.2.5',
                         '-i "F:/Users/James/Documents/House/Electrical/Meter/SDM630/Simple/ACTsdm630.txt"'])


if args.verbose:
    VERBOSE = args.verbose

if args.input:
    DATA = args.input

if args.set:
    if VERBOSE > 0:
        print ('SET action is disabled')
    sys.exit(0)

if args.OID:
    OidReq = args.OID
else:
    if VERBOSE > 0:
        print ('No OID given')
    sys.exit(0)

if args.next:
    Next = True
    if VERBOSE > 0:
        print ('GETNEXT action chosen')

# Check OID Matched
if OidReq.find( OidBase ) != 0 :
    if VERBOSE > 0:
        print ('Incorrect OID given: ' + OidReq)
    sys.exit(0)

# Open data file
if not os.path.isfile(DATA):
    if VERBOSE > 0:
        print (DATA + ' is missing')
    sys.exit(DATA + " does not exist.")
    
sdmdata = configparser.ConfigParser()

try:
    sdmdata.read(DATA)
    
except OSError:
    if VERBOSE > 0:
        print("Could not open " + DATA)
    sys.exit("Could not open " + DATA)

if sdmdata.get('MODBUS','read') != 'SUCCESSFUL' :
    if VERBOSE > 0:
        print("SDM Data is invalid")
    sys.exit("SDM Data is invalid")

# Watt Hours, Cumulative energy usage
# Multiply by 1000 as in kW
dEnergyCon=round( sdmdata.getfloat('MODBUS','IMPO_WH') * 1000)

# Watts, instantaneous usage
dPowerCon=round( sdmdata.getfloat('MODBUS','P_TOT_W') )

# System Voltage
dVoltage=round( sdmdata.getfloat('MODBUS','Avg_Volt'), 2 )	
