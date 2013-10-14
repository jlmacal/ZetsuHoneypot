"""
Copyright (C) 2013  Juan Luis Martin Acal

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los terminos de la Licencia Publica General GNU publicada
por la Fundacion para el Software Libre, ya sea la version 3
de la Licencia, o (a su eleccion) cualquier version posterior.

Este programa se distribuye con la esperanza de que sea util, pero
SIN GARANTIA ALGUNA; ni siquiera la garantia implicita
MERCANTIL o de APTITUD PARA UN PROPOSITO DETERMINADO.
Consulte los detalles de la Licencia Publica General GNU para obtener
una informacion mas detallada.

Deberia haber recibido una copia de la Licencia Publica General GNU
junto a este programa.
En caso contrario, consulte <http://www.gnu.org/licenses/>.


                contact:  jlmacal@gmail.es
"""

from kippo.core import dblog
from twisted.enterprise import adbapi
from twisted.internet import defer
from twisted.python import log
import time
import uuid
import os
from pysqlite2 import dbapi2

class DBLogger(dblog.DBLogger):

	def start(self, cfg):
		self.db = cfg.get('database_sqlite', 'dbfile')
		if not os.path.exists(self.db):
			try:
				connectionBD = dbapi2.connect(self.db)
				connectionBD.execute("""CREATE TABLE "online_sessions_table" (
					"connection_timestamp" FLOAT NOT NULL,
					"session_id" TEXT PRIMARY KEY  NOT NULL  UNIQUE,
					"local_host" TEXT NOT NULL,
					"local_port" INTEGER NOT NULL,
					"remote_host" TEXT NOT NULL,
					"remote_port" INTEGER NOT NULL,
					"terminal_width" INTEGER NOT NULL,
					"terminal_height" INTEGER NOT NULL)""")
				connectionBD.commit()
				connectionBD.execute("""CREATE TABLE "auth_table" (
					"login_timestamp" FLOAT NOT NULL,
					"remote_host" TEXT NOT NULL,
					"login" TEXT NOT NULL,
					"password" TEXT NOT NULL,
					"result" BOOL NOT NULL)""")
				connectionBD.commit()
				connectionBD.execute("""CREATE TABLE "command_table" (
					"command_timestamp" FLOAT NOT NULL,
					"remote_host" TEXT NOT NULL,
					"command" TEXT NOT NULL,
					"known" INTEGER NOT NULL)""")
				connectionBD.commit()
				connectionBD.execute("""CREATE TABLE "client_table" (
					"client_timestamp" FLOAT NOT NULL,
					"remote_host" TEXT NOT NULL,
					"client" TEXT NOT NULL)""")
				connectionBD.commit()
				connectionBD.close()
			except Exception,e:
				print '[EXCEPTION]' + str(e)
				return	

	def write(self, session, msg):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('Module write %s [%s]: %s\r\n' % (session, time.strftime('%Y-%m-%d %H:%M:%S'), msg))
		#test.close()
		###TESTING
		pass

	def createSession(self, peerIP, peerPort, hostIP, hostPort):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule createSession New connection: %s:%s %s:%s\n' % (peerIP, peerPort, hostIP, hostPort))
		#test.close()
		###TESTING

		sid = uuid.uuid1().hex
		#sensorname = self.getSensor() or hostIP

		try:
			connectionBD = dbapi2.connect(self.db)
			cursorInsertion = connectionBD.cursor()	
			stringInsertion = 'INSERT OR IGNORE INTO online_sessions_table (connection_timestamp,session_id,local_host,local_port,remote_host,remote_port,terminal_width,terminal_height) VALUES (?,?,?,?,?,?,?,?)'
			parameters = (time.time(),sid,hostIP,hostPort,peerIP,peerPort,0,0)
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()
			connectionBD.close()
		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

		return sid

	def handleConnectionLost(self, session, args):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule conecctionLost %s\n' % (session))
		#test.close()
		###TESTING

		try:
			connectionBD = dbapi2.connect(self.db)
			cursorInsertion = connectionBD.cursor()	
			stringInsertion = 'DELETE FROM online_sessions_table WHERE session_id=?'
			parameters = (session,)
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()
			connectionBD.close()
		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

	def handleLoginFailed(self, session, args):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule loginFail Login failed [%s/%s]\n' % (args['username'], args['password']))
		#test.close()
		###TESTING

		try:
			connectionBD = dbapi2.connect(self.db)

			cursorSelection = connectionBD.cursor()
			stringSelection = 'SELECT remote_host FROM online_sessions_table WHERE session_id=?'
			parameters = (session,)
			cursorSelection.execute(stringSelection,parameters)
			rowSession = cursorSelection.fetchall()
			connectionBD.commit()

			cursorInsertion = connectionBD.cursor()
			stringInsertion = 'INSERT OR IGNORE INTO auth_table (login_timestamp,remote_host,login,password,result) VALUES (?,?,?,?,?)'
			parameters = (time.time(),rowSession[0][0],args['username'],args['password'],0)
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()

			connectionBD.close()

		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

	def handleLoginSucceeded(self, session, args):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule loginSucceeded Login succeeded [%s/%s]\n' % (args['username'], args['password']))
		#test.close()
		###TESTING

		try:
			connectionBD = dbapi2.connect(self.db)

			cursorSelection = connectionBD.cursor()
			stringSelection = 'SELECT remote_host FROM online_sessions_table WHERE session_id=?'
			parameters = (session,)
			cursorSelection.execute(stringSelection,parameters)
			rowSession = cursorSelection.fetchall()
			connectionBD.commit()

			cursorInsertion = connectionBD.cursor()
			stringInsertion = 'INSERT OR IGNORE INTO auth_table (login_timestamp,remote_host,login,password,result) VALUES (?,?,?,?,?)'
			parameters = (time.time(),rowSession[0][0],args['username'],args['password'],1)
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()

			connectionBD.close()

		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

	def handleCommand(self, session, args):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule comandos Command [%s]\n' % (args['input'],))
		#test.close()
		###TESTING

		try:
			connectionBD = dbapi2.connect(self.db)

			cursorSelection = connectionBD.cursor()
			stringSelection = 'SELECT remote_host FROM online_sessions_table WHERE session_id=?'
			parameters = (session,)
			cursorSelection.execute(stringSelection,parameters)
			rowSession = cursorSelection.fetchall()
			connectionBD.commit()

			cursorInsertion = connectionBD.cursor()
			stringInsertion = 'INSERT OR IGNORE INTO command_table (command_timestamp,remote_host,command,known) VALUES (?,?,?,?)'
			parameters = (time.time(),rowSession[0][0],args['input'],1)
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()

			connectionBD.close()

		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

	def handleUnknownCommand(self, session, args):		
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule unknownCommand Unknown command [%s]\n' % (args['input'],))
		#test.close()
		###TESTING

		try:
			connectionBD = dbapi2.connect(self.db)

			cursorSelection = connectionBD.cursor()
			stringSelection = 'SELECT remote_host FROM online_sessions_table WHERE session_id=?'
			parameters = (session,)
			cursorSelection.execute(stringSelection,parameters)
			rowSession = cursorSelection.fetchall()
			connectionBD.commit()

			cursorInsertion = connectionBD.cursor()
			stringInsertion = 'INSERT OR IGNORE INTO command_table (command_timestamp,remote_host,command,known) VALUES (?,?,?,?)'
			parameters = (time.time(),rowSession[0][0],args['input'],0)
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()

			connectionBD.close()

		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

	def handleInput(self, session, args):		
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule input Input [%s] @%s\n' % (args['input'], args['realm']))
		#test.close()
		###TESTING

		try:
			connectionBD = dbapi2.connect(self.db)

			cursorSelection = connectionBD.cursor()
			stringSelection = 'SELECT remote_host FROM online_sessions_table WHERE session_id=?'
			parameters = (session,)
			cursorSelection.execute(stringSelection,parameters)
			rowSession = cursorSelection.fetchall()
			connectionBD.commit()

			cursorInsertion = connectionBD.cursor()
			stringInsertion = 'INSERT OR IGNORE INTO command_table (command_timestamp,remote_host,command,known) VALUES (?,?,?,?)'
			parameters = (time.time(),rowSession[0][0],args['input'] + " " + args['realm'],2)
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()

			connectionBD.close()

		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

	def handleTerminalSize(self, session, args):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule terminalSize Terminal size: %sx%s\n' % (args['width'], args['height']))
		#test.close()
		###TESTING

		try:
			connectionBD = dbapi2.connect(self.db)
			cursorInsertion = connectionBD.cursor()	
			stringInsertion = 'UPDATE OR IGNORE online_sessions_table SET terminal_width=?,terminal_height=? WHERE session_id=?'
			parameters = (args['width'],args['height'],session)
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()
			connectionBD.close()
		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

	def handleClientVersion(self, session, args):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule clientVersion Client version: [%s]\n' % (args['version'],))
		#test.close()
		###TESTING

		try:
			connectionBD = dbapi2.connect(self.db)

			cursorSelection = connectionBD.cursor()
			stringSelection = 'SELECT remote_host FROM online_sessions_table WHERE session_id=?'
			parameters = (session,)
			cursorSelection.execute(stringSelection,parameters)
			rowSession = cursorSelection.fetchall()
			connectionBD.commit()

			cursorInsertion = connectionBD.cursor()
			stringInsertion = 'INSERT OR IGNORE INTO client_table (client_timestamp,remote_host,client) VALUES (?,?,?)'
			parameters = (time.time(),rowSession[0][0],args['version'])
			cursorInsertion.execute(stringInsertion,parameters)
			connectionBD.commit()

			connectionBD.close()

		except Exception,e:
			print '[EXCEPTION]' + str(e)
			return

	def handleFileDownload(self, session, args):
		###TESTING
		#test = file('/tmp/outputTestKippo.txt', 'a')
		#test.write('\nModule fileDownload File download: [%s] -> %s\n' % (args['url'], args['outfile']))
		#test.close()
		###TESTING
		pass

# vim: set sw=4 et:

