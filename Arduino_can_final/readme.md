##### 10µF between RST & GND
	To prevent reset of the arduino when serial is open with raspberry 
	< https://forum.arduino.cc/t/uno-prevent-reset-when-open-serial-monitor/346618 >
	
##### Radio_POWER_PIN = 3;
	INPUT
	Is the state of the RD4 power
	if true it is a +12v (needed to go to 5Vmax!)
	->if low : arduino send shut down frame to raspberry

##### screenBrightnessPin = 6;
	OUTPUT
	Is a duplication of the dark button of the front radio face

##### screenPowerPin = 7;
	OUTPUT
	Is a duplication of the state of the radio display order from the rd4
