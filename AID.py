#!/usr/bin/python

from pyfiglet import Figlet
import time
import sys
from Server import Ruler
#banner Of the program

command = sys.argv
len_command = len(command)
ascii_banner = Figlet(font='slant')
print(ascii_banner.renderText('TITAN'))

if len_command >= 2:
    if command[1] == 'Toolkit' or 'connect':
        time.sleep(0.5)
        print('Welcome to the RAT(Remote Access Tool) Titan')
        ip = input('Enter your ip address ::>> ')
        port = int(input('Enter a usable port ::>> '))
        rKing = Ruler(ip, port)

else:
    print('Use "--help" for more option')
