import socket
import sys
from datetime import datetime
import atexit 



HOST = '' # localhost
PORT = 23456 # change to your preferred listening port 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.bind((HOST,PORT))
	s.listen(1)
	print "Listening on port", PORT
except:
	s.close() # Free up the port in case
	s = None
	print "Could not open socket"
	sys.exit(1)

conn,addr = s.accept() 
print 'Connected by', addr
conn.send('LOAD')



while 1:
	data = conn.recv(1024)
	if not data: break

	print("=============================================================")
	print(data)
	try:
		imei,_,date,_,fix,time,_,lat,ns,lon,ew,_,_ = data.split(",")

	 	# Not sure if %m is correct for months: don't know how it represents single digit months
		date =  datetime.strptime(date, "%y%m%d%H%M")
		print "Device date/time: ", date

		# Ignoring miliseconds as they appear to be unused by the device
		time = datetime.strptime(time[:6], "%H%M%S")
		print "Time UTC: ",time.strftime("%H%M:%S")
	
		# Removing the 'imei' label in the data
		_,imei = imei.split(":")
		print "IMEI: ", imei

		# Convert to decimal latitude 
		lat = (1 if ns == "N" else -1) * (int(lat[:2]) + float(lat[2:])/60)		
		print "Latitude: ", lat

		# Convert to decimal longitude
		lon = (1 if ew == "E" else -1) * (int(lon[:3]) + float(lon[3:])/60)
		print "Longitude: ", lon

		print "Google Maps Link: http://maps.google.co.uk/?q=%f,%f" % (lat,lon)
		
		f = open("test.kml", "a") 
		string = str(lon) + "," + str(lat) + ",0\n"
		f.write(string)
		f.close()
	except: 
		print "Packet unparsable"
	
	conn.send('ON')
conn.close()

@atexit.register
def close_all():
	conn.close()

