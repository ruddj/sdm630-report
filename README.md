# sdm630-report
Tools for monitoring an SDM630 3 phase meter and reporting output to PVoutput


##Current Features
- Reads current values over MODBUS from a SDM630 digital meter.
- Uploads a generated config file to PVOutput for analyses and graphing
- Can download weather data to include in upload

##Requirements
- USB to RS485 adaptor.
  - I used a USB to RS485 TTL Serial Converter Adapter FTDI interface FT232RL 75176 Module S
- sdm630-usb requires ModBus Libraries
- Scripts are written in Python3
- Python3 script for PVOutput requires requests

##Installation
```bash 
sudo aptitude install libmodbus-dev libmodbus5`
```

Compile with
```bash 
gcc sdm630-usb.c -o sdm630 `pkg-config --cflags --libs libmodbus`
```

###Crontab entries
Edit cron files using **crontab -e**

```cron
*/5 *   *   *   *    /opt/sdm630/sdm630-poll.sh
3-59/5 *   *   *   *    /opt/sdm630/pvoutput.py
2-59/5 *   *   *   *    /opt/sdm630/downloadWeather.sh
```

## TODO
- SNMP extension to allow data collection by Cacti or other SNMP tools
