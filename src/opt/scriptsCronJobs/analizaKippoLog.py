"""
Copyright (C) 2013  Juan Luis Martin Acal

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la Licencia Pública General GNU publicada
por la Fundación para el Software Libre, ya sea la versión 3
de la Licencia, o (a su elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil, pero
SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita
MERCANTIL o de APTITUD PARA UN PROPÓSITO DETERMINADO.
Consulte los detalles de la Licencia Pública General GNU para obtener
una información más detallada.

Debería haber recibido una copia de la Licencia Pública General GNU
junto a este programa.
En caso contrario, consulte <http://www.gnu.org/licenses/>.


                contact:  jlmacal@gmail.es
"""
import sys
import os
import string
import re
import time
import glob
from datetime import datetime
from pysqlite2 import dbapi2
	

def insertaTablaLogin(rutaBD,fechaTimeStamp,tty,ip,login,password,resultado):
	
	try:
		conexionBD = dbapi2.connect(rutaBD)
	except Exception, e:
		print "<excepcion>"+str(e)+"</excepcion>"
		sys.exit(1)
	else:	
		try:
			cursorInsercion = conexionBD.cursor()	
			cadenaInsercion = 'insert or ignore into tablaLogin (fechaTimeStamp,tty,ip,login,password,resultado) values (?,?,?,?,?,?)'
			parametros = (fechaTimeStamp,tty,ip,login,password,resultadoToBinRes(resultado))
			cursorInsercion.execute(cadenaInsercion,parametros)
			conexionBD.commit()
			cursorInsercion.close()
		except Exception, e:
			print "<excepcion>"+str(e)+"</excepcion>"
			cursorInsercion.close()
				
		
def insertaTablaCmd(rutaBD,fechaTimeStamp,sesion,tty,ip,cmd):
	
	try:
		conexionBD = dbapi2.connect(rutaBD)
	except Exception, e:
		print "<excepcion>"+str(e)+"</excepcion>"
		sys.exit(1)
	else:
		try:
			cursorInsercion = conexionBD.cursor()
			cadenaInsercion = 'insert or ignore into tablaCmd (fechaTimeStamp,sesion,tty,ip,cmd) values (?,?,?,?,?)'	
			parametros = (fechaTimeStamp,sesion,tty,ip,cmd.replace("\n",''))
			cursorInsercion.execute(cadenaInsercion,parametros)
			conexionBD.commit()
			cursorInsercion.close()
		except Exception, e:
			print "<excepcion>"+str(e)+"</excepcion>"
			cursorInsercion.close()


def insertaTablaCliente(rutaBD,fechaTimeStamp,tty,ip,cliente):
	
	try:
		conexionBD = dbapi2.connect(rutaBD)
	except Exception, e:
		print str(e)
		sys.exit(1)
	else:
		try:		
			cursorInsercion = conexionBD.cursor()
			cadenaInsercion = 'insert or ignore into tablaCliente (fechaTimeStamp,ip,cliente) values (?,?,?)'	
			parametros = (fechaTimeStamp,ip,cliente)
			cursorInsercion.execute(cadenaInsercion,parametros)
			conexionBD.commit()
			cursorInsercion.close()
		except Exception, e:
			print "<excepcion>"+str(e)+"</excepcion>"
			cursorInsercion.close()


def strToTimeStamp (fecha,hora):
	
	date_str = fecha + " " + hora
	time_tuple = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
	fechaTimeStamp = time.mktime(time_tuple)+0.000001
	
	return fechaTimeStamp


def resultadoToBinRes(resultado):
	
	resBin=None
	if(resultado=="failed"):
		resBin=0
	else:
		resBin=1
	return resBin


def parseaLog(rutaBD,nombreLog):
	
	#2011-04-19 13:36:50+0200 [SSHService ssh-userauth on HoneyPotTransport,1,150.214.21.31] login attempt [root/123] failed
	#2011-04-19 13:36:58+0200 [SSHChannel session (0) on SSHService ssh-connection on HoneyPotTransport,1,150.214.21.31] CMD: prueba2
	#2011-04-19 13:36:44+0200 [HoneyPotTransport,1,150.214.21.31] Remote SSH version: SSH-2.0-PuTTY_Release_0.60
	
	try:
		archivoLog=open(nombreLog,"r")
		patronFechaIpLoginPassSesion = re.compile('(^[0-9\-]+)\s([0-9\:]+)\+[0-9]+ \[SSHService ssh-userauth on HoneyPotTransport,([0-9]+),([0-9.]+)\] login attempt \[([a-zA-Z0-9\-\[\]\#\.\:\%\@\&\_]+)\/([a-zA-Z0-9\-\[\]\#\.\:\%\@\&\_]+)\] ([a-z]+)$')
		patronFechaIpCmd =             re.compile('(^[0-9\-]+)\s([0-9\:]+)\+[0-9]+ \[SSHChannel session \(([0-9]+)\) on SSHService ssh-connection on HoneyPotTransport,([0-9]+),([0-9.]+)\] CMD\: ([a-zA-Z0-9\-\[\]\#\.\:\%\@\&\"\'\_\s\\\/]+)$')
		patronFechaIpClient =          re.compile('(^[0-9\-]+)\s([0-9\:]+)\+[0-9]+ \[HoneyPotTransport,([0-9]+),([0-9.]+)\] Remote SSH version: ([a-zA-Z0-9\-\[\]\#\.\:\%\@\&\_]+)')
			
		for linea in archivoLog:
			
			inicioSesion = re.findall(patronFechaIpLoginPassSesion,linea)
			comandoSesion = re.findall(patronFechaIpCmd,linea)
			clienteSesion = re.findall(patronFechaIpClient,linea)
			if inicioSesion:
				insertaTablaLogin(rutaBD,strToTimeStamp (inicioSesion[0][0],inicioSesion[0][1]),inicioSesion[0][2],inicioSesion[0][3],inicioSesion[0][4],inicioSesion[0][5],inicioSesion[0][6])
				#print inicioSesion
				#pass	
			elif comandoSesion:
				insertaTablaCmd(rutaBD,strToTimeStamp (comandoSesion[0][0],comandoSesion[0][1]),comandoSesion[0][2],comandoSesion[0][3],comandoSesion[0][4],comandoSesion[0][5])
				#print comandoSesion
				#pass
			elif clienteSesion:
				insertaTablaCliente(rutaBD,strToTimeStamp (clienteSesion[0][0],clienteSesion[0][1]),clienteSesion[0][2],clienteSesion[0][3],clienteSesion[0][4])
				#print clienteSesion
				#pass
				
		archivoLog.close()
		
	except Exception, e:
		print "<excepcion>"+str(e)+"<nombre>"+str(nombreLog)+"</nombre>"+"</excepcion>"


def OffKippo(rutaPidFile,rutaDirLogs):
	
	try:
		archivoPid=open(rutaPidFile,"r")
		pid=archivoPid.readline()
		os.kill(int(pid),9)
		archivoPid.close()
		os.system("rm -rf " + rutaDirLogs + "kippo.pid")
	except ValueError:
		os.system("rm -rf " + rutaDirLogs + "kippo.pid")
		print "<excepcion>El fichero kippo.pid no contienen un entero</excepcion>"
		sys.exit(1)
	except Exception, e:
		print str(e)
		sys.exit(1)
		
		
def OnKippo(rutaDirLogs):
	
	try:
		os.system("rm -rf " + rutaDirLogs + "kippo.pid")
		os.system("rm -rf " + rutaDirLogs + "kippo.log*")
		os.system("rm -rf " + rutaDirLogs + "tty/*.log")
		os.system("twistd -y kippo.tac -l log/kippo.log --pidfile kippo.pid")
	except Exception, e:
		print "<excepcion>"+str(e)+"</excepcion>"
		

def main():
	
	rutaBD="log/kippoBD.sqlite"
	rutaDirLogs="log/"
	rutaPidFile="kippo.pid"

	try:
		os.chdir("/opt/kippo")
	except Exception, e:
		print str(e)
		sys.exit(1)	
		
	OffKippo(rutaPidFile,rutaDirLogs)
	for file in glob.glob(rutaDirLogs + "/kippo.log*"): 
		parseaLog(rutaBD,file)
	OnKippo(rutaDirLogs)


if __name__=="__main__":
	main()
