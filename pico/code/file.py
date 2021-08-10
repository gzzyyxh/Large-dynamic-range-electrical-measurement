import machine
import ubinascii
import sys
import os
from machine import Pin, PWM
from time import sleep

print(ubinascii.hexlify(machine.unique_id()))
list = ['a','b','c','fewfwefwe']

# file = open ("D:\\pico\\initialFile.txt", "w")
file = open ("initialFile.txt", "w")
#print(type(file))
#print(os.listdir())
# file.write("Hello \n")
file.write('\n'.join(list))

file.close()

file = open("initialFile.txt", "r")
print(file.read())
file.close()

machine.reset()

