/**
 * USB RS485 of MODBUS info from SDM630 digital meter 
 * Based on code found http://123solar.org/phpBB/viewtopic.php?t=232
 * that was written by Mario Stuetz (mstuetz at gmail.com)
 * Minor modifications below by James Rudd (sdm at jrudd.org)
 * gcc sdm630-usb.c -o sdm630 `pkg-config --cflags --libs libmodbus`
 **/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sysexits.h>
#include <modbus/modbus.h>
#include <sys/resource.h>

#define SERVER_ID 1

float reform_uint16_2_float32(uint16_t u1, uint16_t u2)
{
	uint32_t num = ((uint32_t)u1 & 0xFFFF) << 16 | ((uint32_t)u2 & 0xFFFF);
	float numf;
	memcpy(&numf, &num, 4);
	return numf;
}

int main(int argc, char *argv[]){
	modbus_t *sdm630;
	int iReturn = 0;

	sdm630 = modbus_new_rtu("/dev/ttyUSB0", 9600, 'N', 8, 1);
	modbus_set_slave(sdm630, SERVER_ID);
	modbus_set_debug(sdm630, FALSE);

	if (sdm630 == NULL) {
		fprintf(stderr, "Unable to allocate libmodbus context\n");
		return EX_IOERR; /* 74 input/output error */
	}
	if (modbus_connect(sdm630) == -1) {
		fprintf(stderr, "Connection failed: \n");
		modbus_free(sdm630);
		return EX_NOINPUT; /* 66 cannot open input */
	}
	else if(modbus_connect(sdm630) == 0) {
		// Succesfully Connected 
		printf("[MODBUS]\n");
   }

	uint16_t* catcher = malloc(76*sizeof(uint16_t));
	if(modbus_read_input_registers(sdm630, 0000, 76, catcher)>0){			
		printf("L1_Volt: %f\n",reform_uint16_2_float32(catcher[0],catcher[1]));
		printf("L2_Volt: %f\n",reform_uint16_2_float32(catcher[2],catcher[3]));
		printf("L3_Volt: %f\n",reform_uint16_2_float32(catcher[4],catcher[5]));
		printf("L1_Amps: %f\n",reform_uint16_2_float32(catcher[6],catcher[7]));
		printf("L2_Amps: %f\n",reform_uint16_2_float32(catcher[8],catcher[9]));
		printf("L3_Amps: %f\n",reform_uint16_2_float32(catcher[10],catcher[11]));
		printf("L1_Watt: %f\n",reform_uint16_2_float32(catcher[12],catcher[13]));
		printf("L2_Watt: %f\n",reform_uint16_2_float32(catcher[14],catcher[15]));
		printf("L3_Watt: %f\n",reform_uint16_2_float32(catcher[16],catcher[17]));
		printf("L1_VAac: %f\n",reform_uint16_2_float32(catcher[18],catcher[19]));
		printf("L2_VAac: %f\n",reform_uint16_2_float32(catcher[20],catcher[21]));
		printf("L3_VAac: %f\n",reform_uint16_2_float32(catcher[22],catcher[23]));
		printf("L1_PF: %f\n",reform_uint16_2_float32(catcher[30],catcher[31]));
		printf("L2_PF: %f\n",reform_uint16_2_float32(catcher[32],catcher[33]));
		printf("L3_PF: %f\n",reform_uint16_2_float32(catcher[34],catcher[35]));
		printf("Avg_Volt: %f\n",reform_uint16_2_float32(catcher[42],catcher[43]));
		printf("TOT_Amp: %f\n",reform_uint16_2_float32(catcher[48],catcher[49]));
		printf("P_TOT_W: %f\n",reform_uint16_2_float32(catcher[52],catcher[53]));
		printf("P_FACTO: %f\n",reform_uint16_2_float32(catcher[62],catcher[63]));
		printf("Freq: %f\n",reform_uint16_2_float32(catcher[70],catcher[71]));
		printf("IMPO_WH: %f\n",reform_uint16_2_float32(catcher[72],catcher[73]));
		printf("EXPO_WH: %f\n",reform_uint16_2_float32(catcher[74],catcher[75]));

		printf("READ: SUCCESSFUL\n");
	}
	else{
		printf("READ: FAILED\n");
		iReturn = EX_DATAERR; /* 65 data format error *//* data format error */
	}

	free(catcher);
	modbus_close(sdm630);
	modbus_free(sdm630);

	return iReturn;
}
