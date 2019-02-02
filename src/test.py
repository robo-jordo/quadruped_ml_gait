#!/usr/bin/env python

file = open("evolution1.txt","w") 
for i in range(5):
	file.write("here is ") 
	file.write(str(i))
	file.write("\n")
file.close() 