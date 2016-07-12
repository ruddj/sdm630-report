#!/usr/bin/python3

# Read in SDM630 values and return SNMP

# Modify /etc/snmp/snmpd.conf
#pass .1.3.6.1.4.1.12345.1.1  /usr/bin/python3 /opt/sdm630/sdm630-snmp.py

import datetime
import os.path
import sys, getopt
import configparser
import argparse
__author__ = 'James Rudd'

DATA="/var/tmp/ACTsdm630.txt"
OidBase = ".1.3.6.1.4.1.12345.1.1"; 
VERBOSE = 0
Next = False

# Arguments
parser = argparse.ArgumentParser(description='Script to return consumption data to SNMP')
parser.add_argument('-v', '--verbose', help = 'Verbose Level. -vv = Very Verbose', action = 'count')
parser.add_argument('-i', '--input', help = 'Input consumption data file')
parser.add_argument('-s', '--set', help = 'SNMP Set (no action)')
parser.add_argument('-g', '--get', help = 'SNMP Get (Default)', action='store_true')
parser.add_argument('-n', '--next', help = 'SNMP GetNext - determine next valid instance', action='store_true')
parser.add_argument('OID', help = "SNMP OID to retrieve. Should begin with " + OidBase)

args = parser.parse_args()

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

# List of OIDs
Oids = [
    OidBase,
    OidBase + ".1.0",
    OidBase + ".1.1.1",
    OidBase + ".1.1.2",
    OidBase + ".1.1.3",
    OidBase + ".1.2.1",
    OidBase + ".1.2.2",
    OidBase + ".1.2.3",
    OidBase + ".2.0",
    OidBase + ".2.1.1",
    OidBase + ".2.1.2",
    OidBase + ".2.1.3",
    OidBase + ".2.2.1",
    OidBase + ".2.2.2",
    OidBase + ".2.2.3",
    OidBase + ".3.0",
    OidBase + ".3.1.1",
    OidBase + ".3.1.2",
    OidBase + ".3.1.3",
    OidBase + ".3.2.1",
    OidBase + ".3.2.2",
    OidBase + ".3.2.3",
    OidBase + ".4.0",
    OidBase + ".4.1.1",
    OidBase + ".4.1.2",
    OidBase + ".4.1.3",
    OidBase + ".4.2.1",
    OidBase + ".4.2.2",
    OidBase + ".4.2.3",
    OidBase + ".5.0",
    OidBase + ".5.1.1",
    OidBase + ".5.1.2",
    OidBase + ".5.1.3",
    OidBase + ".5.2.1",
    OidBase + ".5.2.2",
    OidBase + ".5.2.3",
    OidBase + ".6.0",
    OidBase + ".6.1",
    OidBase + ".7.0",
    OidBase + ".7.1",
    OidBase + ".8.0",
    OidBase + ".8.1",
    OidBase + ".9.0",
    OidBase + ".9.1",
    OidBase + ".10.0",
    OidBase + ".10.1",
    OidBase + ".11.0",
    OidBase + ".11.1",
    OidBase + ".12.0",
    OidBase + ".12.1",
]

#
#  GETNEXT requests - determine next valid instance
#
if Next == True:

    try:
        OidReqIndex = Oids.index(OidReq) + 1
    except ValueError as ve:
        if VERBOSE > 0:
            print("OID error: " + str(ve))
        sys.exit() 

    if OidReqIndex >= len(Oids):
        if VERBOSE > 0:
            print("No GETNEXT Value")
        sys.exit()       

    OidReq = Oids[OidReqIndex]


else:
    #
    #  GET requests - check for valid instance
    #
    try:
        OidReqIndex = Oids.index(OidReq)
    except ValueError as ve:
        if VERBOSE > 0:
            print("Invalid OID error: " + str(ve))
        sys.exit() 


#
#  "Process" GET* requests - return config values
#
print (OidReq)

try:
    if OidReq == OidBase :
        print ("string\SDM630-Data")
        sys.exit(0)
    if OidReq == OidBase + ".1.0":
        print ("string\nVoltage")
        sys.exit(0)
    elif OidReq == OidBase + ".1.1.1":
        print ("string\nL1-Voltage")
        sys.exit(0)
    elif OidReq == OidBase + ".1.1.2":
        print ("string\nL2-Voltage")
        sys.exit(0)
    elif OidReq == OidBase + ".1.1.3":
        print ("string\nL3-Voltage")
        sys.exit(0)
    elif OidReq == OidBase + ".1.2.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L1_Volt') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".1.2.2":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L2_Volt') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".1.2.3":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L3_Volt') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".2.0":
        print ("string\nCurrent")
        sys.exit(0)
    elif OidReq == OidBase + ".2.1.1":
        print ("string\nL1-Amps")
        sys.exit(0)
    elif OidReq == OidBase + ".2.1.2":
        print ("string\nL2-Amps")
        sys.exit(0)
    elif OidReq == OidBase + ".2.1.3":
        print ("string\nL3-Amps")
        sys.exit(0)
    elif OidReq == OidBase + ".2.2.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L1_Amps') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".2.2.2":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L2_Amps') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".2.2.3":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L3_Amps') ) )
        sys.exit(0)


    elif OidReq == OidBase + ".3.0":
        print ("string\nEnergy")
        sys.exit(0)
    elif OidReq == OidBase + ".3.1.1":
        print ("string\nL1-Watts")
        sys.exit(0)
    elif OidReq == OidBase + ".3.1.2":
        print ("string\nL2-Watts")
        sys.exit(0)
    elif OidReq == OidBase + ".3.1.3":
        print ("string\nL3-Watts")
        sys.exit(0)
    elif OidReq == OidBase + ".3.2.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L1_Watt') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".3.2.2":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L2_Watt') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".3.2.3":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L3_Watt') ) )
        sys.exit(0)


    elif OidReq == OidBase + ".4.0":
        print ("string\nEnergy VA")
        sys.exit(0)
    elif OidReq == OidBase + ".4.1.1":
        print ("string\nL1-VoltAmps")
        sys.exit(0)
    elif OidReq == OidBase + ".4.1.2":
        print ("string\nL2-VoltAmps")
        sys.exit(0)
    elif OidReq == OidBase + ".4.1.3":
        print ("string\nL3-VoltAmps")
        sys.exit(0)
    elif OidReq == OidBase + ".4.2.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L1_VAac') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".4.2.2":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L2_VAac') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".4.2.3":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L3_VAac') ) )
        sys.exit(0)


    elif OidReq == OidBase + ".5.0":
        print ("string\nPower Factor")
        sys.exit(0)
    elif OidReq == OidBase + ".5.1.1":
        print ("string\nL1-PF")
        sys.exit(0)
    elif OidReq == OidBase + ".5.1.2":
        print ("string\nL2-PF")
        sys.exit(0)
    elif OidReq == OidBase + ".5.1.3":
        print ("string\nL3-PF")
        sys.exit(0)
    elif OidReq == OidBase + ".5.2.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L1_PF') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".5.2.2":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L2_PF') ) )
        sys.exit(0)
    elif OidReq == OidBase + ".5.2.3":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','L3_PF') ) )
        sys.exit(0)

    elif OidReq == OidBase + ".6.0":
        print ("string\nAvg Volt")
        sys.exit(0)
    elif OidReq == OidBase + ".6.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','Avg_Volt') ) )
        sys.exit(0)

    elif OidReq == OidBase + ".7.0":
        print ("string\nTotalAmps")
        sys.exit(0)
    elif OidReq == OidBase + ".7.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','TOT_Amp') ) )
        sys.exit(0)

    elif OidReq == OidBase + ".8.0":
        print ("string\nTotalWatts")
        sys.exit(0)
    elif OidReq == OidBase + ".8.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','P_TOT_W') ) )
        sys.exit(0)

    elif OidReq == OidBase + ".9.0":
        print ("string\nTotalPowerFactor")
        sys.exit(0)
    elif OidReq == OidBase + ".9.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','P_FACTO') ) )
        sys.exit(0)

    elif OidReq == OidBase + ".10.0":
        print ("string\nFrequency")
        sys.exit(0)
    elif OidReq == OidBase + ".10.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','Freq') ) )
        sys.exit(0)

    elif OidReq == OidBase + ".11.0":
        print ("string\nImportCumulativeWHr")
        sys.exit(0)
    elif OidReq == OidBase + ".11.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','IMPO_WH') ) )
        sys.exit(0)

    elif OidReq == OidBase + ".12.0":
        print ("string\nExportCumulativeWHr")
        sys.exit(0)
    elif OidReq == OidBase + ".12.1":
        print ("string\n{:.2f}".format( sdmdata.getfloat('MODBUS','EXPO_WH') ) )
        sys.exit(0)


    else :
        print ("string\nack... " + OidReq )
        sys.exit(0)   # Should not happen

except Exception as e:
    if VERBOSE > 0:
        print("Key Error: " + str(e))
    sys.exit("Error: " + str(e))