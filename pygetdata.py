# -*- coding: utf-8 -*-
###################################################################################
# Programm PyGetData for getting data from CipherLAB terminals 800x series. Programm is crossplatform. Uses module PySerial.   #
# Usage: pygetdata.py <mode> <port> <file_to_write>                                                                            
# Arguments:                                                                                                                   
#    mode - If 'local' uses local machine port. If 'remote' uses url.                                                            
#    port - 'COMxx' for Win, '/dev/ttyxx' Linux if  'mode' is 'local'                                                         
#               or url like 'socket://xx.xx.xx.xx:xxxx' for remote.                                                           
#    file_to_write - file for writing received data.										
# IMPORTANT 		##############												
#  PyGetData for remote need 'tcp_serial_redirect.py' from PySerial examples from linux to be run.        			
#    usage: tcp_serial_redirect.py --port=/dev/ttyS0 --baud=38400								
# Mobile Computers 8001L on Linux works on port 38400 ports above refused to work.						#
###################################################################################
import serial
import sys
import os
import uuid
import os.path

class getdata:
	nname = ""
	ctx = ""
	def checksumcheck(self,summbyte,firstbyte,checkbyte1,checkbyte2):
		check1=round((firstbyte+summbyte)/256)
		check2=round((firstbyte+summbyte)%256)
		if check1==13 :
			check1==14
		if check2==13 :
			check2=14
		return (check1-checkbyte1)+(check2-checkbyte2)  
	
	def file(self,file):
		if os.name == "posix":
			if file[0:3] == "smb":
				try:
					f = self.ctx.open(file, os.O_CREAT | os.O_APPEND | os.O_WRONLY)
				except:
					raise Exception("Нет доступа к файлу!")
			else:
				try:
					f = open(file, "w")
				except Exception as inst:
					raise Exception(inst)
		else:
			try:
				f = open(file, "w")
			except:
				raise Exception("Нет доступа к файлу!")
		return f

	def recieve(self, port, path, nameoffile):
		if os.name == "posix":
			import smbc
			self.ctx = smbc.Context()
			slash = "/"
		else:
			slash = "\\"
			
		namestring = str(uuid.uuid1())
		name = namestring
		if nameoffile == "":
			nameoffile = namestring

		try:
				ser = serial.Serial(port, 38400, timeout=0.1) #38400
		except:
			raise  Exception("Не могу подключить " + port)
			
		if ser.isOpen() == False:
			raise  Exception("Не могу открыть " + port)

		ser.write("READ\r")
		ser.flush()
		rec = ser.read(4)
		ser.flush()
		cc = -1
		if rec[:3]!="ACK" :
			#error = u"Не могу получить данные!"
			raise  Exception("Не могу получить данные!")

		print str(path)+ "temp" + slash + str(name) + ".txt"
		f = self.file(str(path)+ "temp" + slash + str(name) + ".txt")
		self.nname = nameoffile

		while rec[:4] != "OVER":
			rec = ser.read(30)
			ser.flush()
			db = rec[1:-3]
			bs = 0
			cc+=1
			if cc == 10:
				cc = 0	
			for x in db:
				bs = bs + ord(x)
			if self.checksumcheck(bs,ord(rec[0]),ord(rec[-3]),ord(rec[-2]))!=0:
				cc=-1
				ser.write("NAK\r")
				ser.flush()
				continue
			if ord(rec[0]) != cc:
				cc=-1
				ser.write("NAK\r")
				ser.flush()
				continue
			#print str(cc) + " : " + str(db)
			f.write(db)
			f.write("\n")
			ser.write("ACK\r")
			ser.flush()
		f.close()
		ser.close()
		
		flag = self.file(str(path)+ "temp"+ slash +"start.flg")
		flag.write(str(name))
		flag.write("\n")
		flag.write(str(nameoffile))
		flag.close()
	
	def __init__(self, port, path, nameoffile):
		self.recieve(port, path, nameoffile)

#if __name__ == "__main__":
#	getdata()
