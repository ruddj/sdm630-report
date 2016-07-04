# sdm630-report
Tools for monitoring an SDM630 3 phase meter and reporting output to PVoutput


sdm630-usb requires ModBus Libraries
# sudo aptitude install libmodbus-dev libmodbus5

Compile with
# gcc sdm630-usb.c -o sdm630 `pkg-config --cflags --libs libmodbus`


