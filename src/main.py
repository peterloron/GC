#!/usr/bin/python
# encoding: utf-8
"""
Mightyohm Geiger Counter serial interface

Created by Peter Loron on 2011-10-06.
"""
import ConfigParser
import logging
import sys
import serialReader
import pachube
import time
import Queue
import traceback

CONFIG_FILE = "config.txt"
config = None
log_file = "console"
log_level = logging.WARN


def ReadConfiguration():
    global CONFIG_FILE
    global persistance_modules
    global log_level
    global log_file
    
    try:
        config = ConfigParser.SafeConfigParser()
        config.read(CONFIG_FILE)
        
        log_level = config.get("core","log_level")
        log_file = config.get("core","log_file")

    except Exception, e:
        print("Could not read config: \n\n" + e)
        sys.exit(1)
    finally:
        return config



########################################################

def main():
    global log_level
    global log_file
    global config
    
    # load config from disk
    config = ReadConfiguration()   
    
    # define and configure logging
    LEVELS = { 'debug':logging.DEBUG,
                'info':logging.INFO,
                'warning':logging.WARNING,
                'error':logging.ERROR,
                'critical':logging.CRITICAL,
                }
    
    ll = LEVELS.get(log_level, logging.NOTSET)
    if log_file == 'console':
        logging.basicConfig(level=ll, format="%(asctime)s -- %(message)s")
    else:
        logging.basicConfig(level=ll, format="%(asctime)s -- %(message)s", filename=log_file)



    # this is there the raw data from the serial reader will live until processed
    raw_data = Queue.Queue()

    try:
        # set up and start the serial reader thread
        sr = serialReader.SerialReader(config,raw_data)
        sr.setDaemon(True)
        sr.start()
        
        # set up and start the data processor thread
        pc = pachube.Pachube(config,raw_data)
        pc.setDaemon(True)
        pc.start()
        
        
        # now that we're running, just wait for an interrupt...
        logging.info("Threads initialized. Running...")
        while(True):
            time.sleep(1)
        
    except KeyboardInterrupt:
        logging.debug("Keyboard interrupt caught. Stopping threads.")
        sr.stop_thread()
        pc.stop_thread()
    finally:
        logging.info("Done.")
        pass

    
if __name__ == '__main__':
    main()

