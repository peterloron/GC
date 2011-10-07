#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Peter Loron on 2010-12-25.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import serial
import ConfigParser
import logging
import sys

logging.basicConfig(level=logging.INFO)

port = ""
speed = 0
con = serial.Serial()


def ReadConfiguration():
    global port
    global speed

    try:
        config = ConfigParser.SafeConfigParser()
        config.read('config.txt')
    
        port = config.get("serial", "port")
        speed = config.get("serial","speed")
    except Exception, e:
        logging.error("Could not read config: \n\n%s" % (e))
        sys.exit(1)      


def OpenSerialConnection():
    global speed
    global port
    global con
    
    try:
        con.port = port
        con.speed = speed
        con.timeout = 5
        con.open()
    except serial.SerialException, e:
        logging.error("Could not open serial port %s: \n\n%s" % (con.portstr, e))
        sys.exit(1)    


def CloseSerialConnection():
    global con
    con.close()


def ReadSerialData():
    global con
    
    try:
        # loop-a-doop!
        while True:
            s = con.readline()
            print u"Got some!"
            #f.write(s)
            #f.flush()
    except Exception, e:
        logging.error("Failure while reading serial data.\n\n%s" % (e,))
        

########################################################

ReadConfiguration()
OpenSerialConnection()
CloseSerialConnection()

