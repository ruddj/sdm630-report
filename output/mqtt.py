#!/usr/bin/python3

# Run after SDM630 poll and send data to MQTT broker

import configparser
import platform  # For Hostname
import os.path

import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish

dataFilePath = "/var/tmp/ACTsdm630.txt"
CONFIG = "/etc/sdm630.conf"
VERBOSE = 3
brokerAddress="127.0.0.1" 
brokerDomain = "" # Not working at present and not compat with multiple publish
brokerUser = ""
brokerPass = ""
brokerClient = platform.node()
brokerTopicBase = "power/edb"

# Set system variables

# Open config file
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


if config.has_option('mqtt', 'Domain'):
    brokerDomain = config.get('mqtt', 'Domain', fallback=brokerDomain)

if  config.has_option('mqtt', 'Broker'):
    brokerAddress = config.get('mqtt', 'Broker', fallback=brokerAddress)
    
if config.has_option('mqtt', 'Topic'):
    brokerTopicBase = config.get('mqtt', 'Topic', fallback=brokerTopicBase)	
    
if config.has_option('mqtt', 'User'):
    brokerUser = config.get('mqtt', 'User')	  
    if config.has_option('mqtt', 'Password'):
        brokerPass = config.get('mqtt', 'Password')	  

		
# Load in Data file

if not os.path.isfile(dataFilePath):
    if VERBOSE > 0:
        print (dataFilePath + ' is missing')
    sys.exit(dataFilePath + " does not exist.")
	
# Open data file	
sdmdata = configparser.ConfigParser()

try:
	sdmdata.read(dataFilePath)
		
except OSError:
	print("Could not open " + dataFilePath)
	sys.exit(dataFilePath + " could not be opened.")

if sdmdata.get('MODBUS','read') != 'SUCCESSFUL' :
	print("SDM Data " + dataFilePath + " is invalid")
	sys.exit(dataFilePath + " is invalid.")

# Read Values Needed

mqttValues = list()
# Phase Info
for phase in range(1, 4):
  phaseBase = "%s/phase%d" % (brokerTopicBase, phase)
  mqttValues.append((phaseBase + "/volt", round( sdmdata.getfloat('MODBUS', "L%d_Volt" % (phase)), 2 ) ))
  mqttValues.append((phaseBase + "/amp", round( sdmdata.getfloat('MODBUS', "L%d_Amps" % (phase)), 3 ) ))
  mqttValues.append((phaseBase + "/watt", round( sdmdata.getfloat('MODBUS', "L%d_Watt" % (phase)), 2 ) ))
  mqttValues.append((phaseBase + "/va", round( sdmdata.getfloat('MODBUS', "L%d_VAac" % (phase)), 2 ) ))
  mqttValues.append((phaseBase + "/pf", round( sdmdata.getfloat('MODBUS', "L%d_PF" % (phase)), 4 ) ))


# Meter totals and Averages
phaseBase = "%s/total" % (brokerTopicBase)

# Watt Hours, Cumulative energy usage
# Multiply by 1000 as in kW
mqttValues.append((phaseBase + "/import", round( sdmdata.getfloat('MODBUS','IMPO_WH') * 1000, 3), 0, True))
# Export Power, always 0 as Solar on other side of meter
mqttValues.append((phaseBase + "/export", round( sdmdata.getfloat('MODBUS','EXPO_WH') * 1000, 3), 0, True))

# Watts, instantaneous usage
mqttValues.append((phaseBase + "/watt", round( sdmdata.getfloat('MODBUS','P_TOT_W') ) ))

# System Voltage
mqttValues.append((phaseBase + "/volt", round( sdmdata.getfloat('MODBUS','Avg_Volt'), 2 ) ))

# Total Current
mqttValues.append((phaseBase + "/amp", round( sdmdata.getfloat('MODBUS','TOT_Amp'), 2 ) ))

# Average Power Factor
mqttValues.append((phaseBase + "/pf", round( sdmdata.getfloat('MODBUS','P_FACTO'), 4 ) ))

# Average Frequency
mqttValues.append((phaseBase + "/freq", round( sdmdata.getfloat('MODBUS','Freq'), 2 ) ))


#Send to MQTT



#broker_address="iot.eclipse.org" #use external broker
#client = mqtt.Client(brokerClient) #create new instance
#client.tls_set()
#client.username_pw_set(brokerUser, brokerPass)
#client.connect(brokerAddress, port=8883) #connect to broker
#client.connect_srv(brokerDomain) #connect to broker

#client.publish(publishBase . "house/main-light","OFF")#publish

# ###

# Alter multiple publish

if VERBOSE > 2:
	print("List for MQTT")
	print( mqttValues )
		
mqttAuth = None
if (brokerUser != ""):
	mqttAuth = {'username':brokerUser, 'password':brokerPass}
		
publish.multiple(mqttValues, port=1883, hostname=brokerAddress, client_id=brokerClient, auth=mqttAuth)

