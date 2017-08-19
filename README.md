# sdm630-report
Tools for monitoring an SDM630 3 phase meter and reporting output to PVoutput

Main C code is from Mario Stuetz in thread  [123solar Eastron SDM630 DC](http://123solar.org/phpBB/viewtopic.php?t=232)

## Current Features
- Reads current values over MODBUS from a Eastron SDM630 digital meter and exports to an ini file
- Uploads data to PVOutput for analyses and graphing
- Can download weather data to include in upload

## Requirements
- Eastron SDM630 DC installed in main switchboard
- USB to RS485 adaptor.
  - I used a USB to RS485 TTL Serial Converter Adapter FTDI interface FT232RL 75176 Module S
- Or a TCp-RS485 e.g. Q14870 USR-TCP232-304 or Q00194 USR-TCP232-24
- sdm630-usb requires ModBus Libraries
- Scripts are written in Python3
- Python3 script for PVOutput requires requests

## Installation
1. If installing on Raspberry Pi, I suggest using a ram disk for storage to prevent wear on SD card.

  1. Create a tmp directory mount point for RAM disk

	```bash
	sudo mkdir /var/tmp
	```

  2. Add the following to bottom of */etc/fstab*

	```
	tmpfs /var/tmp tmpfs nodev,nosuid,size=1M 0 0
	```

  3. Mount the RAM disk to create it

	```bash
	sudo mount /var/tmp
	```

1. Install libraries for modbus

	```bash
	sudo aptitude install libmodbus-dev libmodbus5`
	```

	Compile with
	```bash
	gcc sdm630-usb.c -o sdm630 `pkg-config --cflags --libs libmodbus`
	```

1. Copy files

	```bash
	sudo mkdir /opt/sdm630
	sudo cp config/sdm630.conf /etc/
	sudo cp import/* /opt/sdm630/
	sudo cp output/* /opt/sdm630/
	```

### Crontab entries
Edit cron files using **crontab -e**

```cron
*/5 *   *   *   *    /opt/sdm630/sdm630-poll.sh
3-59/5 *   *   *   *    /opt/sdm630/pvoutput.py
2-59/5 *   *   *   *    /opt/sdm630/downloadWeather.sh
```

## TODO
- SNMP extension to allow data collection by Cacti or other SNMP tools
