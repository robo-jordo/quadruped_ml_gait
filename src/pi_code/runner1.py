#!/usr/bin/env python
import smbus, time
bus = smbus.SMBus(1)
addr = 0x40

best = [2, -5, -5, -6, 4, -3, 4, 5, -5, 5, 5, 0, 6, -3, 1, 5, -6, -6, 3, -6, -1, -6, 6, -1, 0, 2, -4, -2, -6, 3, 0, 4, 3, 6, -5, -3, 2, -2, -4, 0, -3, -5, 6, -4, 4, 1, 4, 0, -2, -4, 2, -5, 1, -4, 0, -2, 2, -3, -1, -4, -5, 1, -6, 2, -5, 6, 6, -1, 0, 1, -1, 4, 1, -4, -5, 6, -2, -3, 5, 1, -1, 1, 3, 4, -3, -3, -1, -1, -2, -3, -5, -2, -2, -4, 4, 3, 0, -2, -6, -4, 5, -1, -4, 2, -3, 6, -5, -6, -3, 4, 2, 6, -1, -2, 3, -6, 1, -4, 5, 1, -4, -6, -4, -1, 3, -5, 6, -3, 4, -6, 2, -5, -3, -6, 2, -1, -2, -1, 5, -6, 4, -2, 2, -5, 1, -6, -3, -2, 1, 1, 1, -6, 6, -5, -6, 3, -3, 3, 4, -4, -2, -4, 6, -6, 4, -2, -6, -2, -3, -6, 2, 4, -5, -5, 6, -1, 6, 0, -6, 5, -3, -1, -5, -3, 4, 5, 1, 0, 5, 2, 6, 1, 4, 5, -3, 2, 3, 6, -6, 1, 2, -4, 5, 5, -1, 6, 3, -6, 2, 3, 2, 1, -6, 3, -6, -2, -5, -2, -1, -2, 2, -6, -4, -4, 5, 0, -4, -4, 1, -3, -4, -6, -3, 0, 6, 5, 2, -1, 1, -1, -1, -6, -5, -5, -5, 4, 3, 4, 3, 1, -5, 2, 4, 2, 0, 3]
limit = 1.6



bus.write_byte_data(addr, 0, 0x20) # enable the chip
time.sleep(.25)
bus.write_byte_data(addr, 0, 0x10) # enable Prescale change as noted in the datasheet
time.sleep(.25) # delay for reset
bus.write_byte_data(addr, 0xfe, 0x79) #changes the Prescale register value for 50 Hz, using the equation in the datasheet.
bus.write_byte_data(addr, 0, 0x20) # enables the chip

time.sleep(.25)
for i in range(12):
	bus.write_word_data(addr, 0x06+i*0x04, 0) # chl 0 start time = 0us
	time.sleep(.25)

for i in range(len(best)):
	if(i%8==0):
		bus.write_word_data(addr, 0x08, (best[i]/6.0+1)*limit) # chl 0 end time = 1.0ms (0 degrees)
		bus.write_word_data(addr, 0x0C, (best[i+1]/6.0+1)*limit)
		bus.write_word_data(addr, 0x10, (best[i+2]/6.0+1)*limit)
		bus.write_word_data(addr, 0x14, (best[i+3]/6.0+1)*limit)
		bus.write_word_data(addr, 0x18, (best[i+4]/6.0+1)*limit)
		bus.write_word_data(addr, 0x1C, (best[i+5]/6.0+1)*limit)
		bus.write_word_data(addr, 0x20, (best[i+6]/6.0+1)*limit)
		bus.write_word_data(addr, 0x24, (best[i+7]/6.0+1)*limit)
		time.sleep(0.8)