##### Radio_POWER_PIN = 3;
	INPUT
	is connected to the +12v (needed to go to 5Vmax!)
	if low : arduino send shut down frame to raspberry

##### Relay_PIN = 4;
	OUTPUT
	is connected to control of power relay 
	is put to high when arduino is up
	goes to down when raspberry shuts down and arduino connected to it goes down too

##### screenBrightnessPin = 6;
	OUTPUT
	Is a duplication of the dark button of the front radio face

##### screenPowerPin = 7;
	OUTPUT
	Is a duplication of the state of the radio 
