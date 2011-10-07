import serial
import ConfigParser

port = ""
speed = 0



def ReadConfiguration():
    global port
    global speed
    
    config = ConfigParser.SafeConfigParser()
    config.read('config.txt')
    
    port = config.get("serial", "port")
    speed = config.get("serial","speed")

port = serial.Serial('')
