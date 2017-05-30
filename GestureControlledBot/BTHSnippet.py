import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM4' 		## need to check at device manager
ser
ser.open()
ser.write(b'Hello World')
ser.close()