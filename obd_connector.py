import obd
from obd import OBDStatus
import time

'''
connection = obd.OBD() # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
print(response.value.to("mph")) # user-friendly unit conversions

'''
'''

#obd.logger.setLevel(obd.logging.DEBUG)

ports = obd.scan_serial()      # return list of valid USB or RF ports
#print(ports)
connection = obd.OBD(ports[1])

#cmd = obd.commands.SPEED # select an OBD command (sensor)
cmd = obd.commands.SPEED

response = connection.query(cmd) # send the command, and parse the response

#print(response.value) # returns unit-bearing values thanks to Pint
print(response.value.to("mph")) # user-friendly unit conversions
'''

ports = obd.scan_serial()
print(ports)
connection = obd.Async(ports[1]) # same constructor as 'obd.OBD()'

def new_speed(r):
    print (r.value.to("mph"))

connection.watch(obd.commands.SPEED, callback=new_speed) # keep track of the RPM
connection.start() # start the async update loop

print(connection.query(obd.commands.RPM)) # non-blocking, returns immediately

time.sleep(60)
connection.stop()