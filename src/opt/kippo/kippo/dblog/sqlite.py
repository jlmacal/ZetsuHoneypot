from kippo.core import dblog
from twisted.enterprise import adbapi
from twisted.internet import defer
from twisted.python import log
import time
import uuid
from pysqlite2 import dbapi2

class DBLogger(dblog.DBLogger):

    def start(self, cfg):
        self.db = cfg.get('database_sqlite', 'dbfile') 

    def write(self, session, msg):
		###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('Modulo write %s [%s]: %s\r\n' % (session, time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        #prueba.close()
        ###DEPURACION
		pass

    def createSession(self, peerIP, peerPort, hostIP, hostPort):
        ###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo createSession New connection: %s:%s %s:%s\n' % (peerIP, peerPort, hostIP, hostPort))
        #prueba.close()
        ###DEPURACION

        sid = uuid.uuid1().hex
        #sensorname = self.getSensor() or hostIP

        try:
            conexionBD = dbapi2.connect(self.db)
            cursorInsercion = conexionBD.cursor()	
            cadenaInsercion = 'INSERT OR IGNORE INTO tablaSesionesOnline (fechaTimeStamp,sesionId,hostLocal,puertoLocal,hostRemoto,puertoRemoto,terminalWidth,terminalHeight) VALUES (?,?,?,?,?,?,?,?)'
            parametros = (time.time(),sid,hostIP,hostPort,peerIP,peerPort,0,0)
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()
        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

        return sid

    def handleConnectionLost(self, session, args):
        ###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo conecctionLost %s\n' % (session))
        #prueba.close()
        ###DEPURACION
        
        try:
            conexionBD = dbapi2.connect(self.db)
            cursorInsercion = conexionBD.cursor()	
            cadenaInsercion = 'DELETE FROM tablaSesionesOnline WHERE sesionId=?'
            parametros = (session,)
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()
        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

    def handleLoginFailed(self, session, args):
		###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo loginFail Login failed [%s/%s]\n' % (args['username'], args['password']))
        #prueba.close()
        ###DEPURACION

        try:
            conexionBD = dbapi2.connect(self.db)

            cursorSeleccion = conexionBD.cursor()
            cadenaSeleccion = 'SELECT hostRemoto FROM tablaSesionesOnline WHERE sesionId=?'
            parametros = (session,)
            cursorSeleccion.execute(cadenaSeleccion,parametros)
            rowSesion = cursorSeleccion.fetchall()
            conexionBD.commit()
            cursorSeleccion.close()

            cursorInsercion = conexionBD.cursor()
            cadenaInsercion = 'INSERT OR IGNORE INTO tablaLogin (fechaTimeStamp,hostRemoto,login,password,resultado) VALUES (?,?,?,?,?)'
            parametros = (time.time(),rowSesion[0][0],args['username'],args['password'],0)
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()

        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

    def handleLoginSucceeded(self, session, args):
		###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo loginSucceeded Login succeeded [%s/%s]\n' % (args['username'], args['password']))
        #prueba.close()
        ###DEPURACION

        try:
            conexionBD = dbapi2.connect(self.db)

            cursorSeleccion = conexionBD.cursor()
            cadenaSeleccion = 'SELECT hostRemoto FROM tablaSesionesOnline WHERE sesionId=?'
            parametros = (session,)
            cursorSeleccion.execute(cadenaSeleccion,parametros)
            rowSesion = cursorSeleccion.fetchall()
            conexionBD.commit()
            cursorSeleccion.close()

            cursorInsercion = conexionBD.cursor()
            cadenaInsercion = 'INSERT OR IGNORE INTO tablaLogin (fechaTimeStamp,hostRemoto,login,password,resultado) VALUES (?,?,?,?,?)'
            parametros = (time.time(),rowSesion[0][0],args['username'],args['password'],1)
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()

        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

    def handleCommand(self, session, args):
		###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo comandos Command [%s]\n' % (args['input'],))
        #prueba.close()
        ###DEPURACION

        try:
            conexionBD = dbapi2.connect(self.db)

            cursorSeleccion = conexionBD.cursor()
            cadenaSeleccion = 'SELECT hostRemoto FROM tablaSesionesOnline WHERE sesionId=?'
            parametros = (session,)
            cursorSeleccion.execute(cadenaSeleccion,parametros)
            rowSesion = cursorSeleccion.fetchall()
            conexionBD.commit()
            cursorSeleccion.close()

            cursorInsercion = conexionBD.cursor()
            cadenaInsercion = 'INSERT OR IGNORE INTO tablaCmd (fechaTimeStamp,hostRemoto,cmd,reconocido) VALUES (?,?,?,?)'
            parametros = (time.time(),rowSesion[0][0],args['input'],1)
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()

        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

    def handleUnknownCommand(self, session, args):		
		###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo unknownCommand Unknown command [%s]\n' % (args['input'],))
        #prueba.close()
        ###DEPURACION

        try:
            conexionBD = dbapi2.connect(self.db)

            cursorSeleccion = conexionBD.cursor()
            cadenaSeleccion = 'SELECT hostRemoto FROM tablaSesionesOnline WHERE sesionId=?'
            parametros = (session,)
            cursorSeleccion.execute(cadenaSeleccion,parametros)
            rowSesion = cursorSeleccion.fetchall()
            conexionBD.commit()
            cursorSeleccion.close()

            cursorInsercion = conexionBD.cursor()
            cadenaInsercion = 'INSERT OR IGNORE INTO tablaCmd (fechaTimeStamp,hostRemoto,cmd,reconocido) VALUES (?,?,?,?)'
            parametros = (time.time(),rowSesion[0][0],args['input'],0)
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()

        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

    def handleInput(self, session, args):		
		###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo input Input [%s] @%s\n' % (args['input'], args['realm']))
        #prueba.close()
        ###DEPURACION

        try:
            conexionBD = dbapi2.connect(self.db)

            cursorSeleccion = conexionBD.cursor()
            cadenaSeleccion = 'SELECT hostRemoto FROM tablaSesionesOnline WHERE sesionId=?'
            parametros = (session,)
            cursorSeleccion.execute(cadenaSeleccion,parametros)
            rowSesion = cursorSeleccion.fetchall()
            conexionBD.commit()
            cursorSeleccion.close()

            cursorInsercion = conexionBD.cursor()
            cadenaInsercion = 'INSERT OR IGNORE INTO tablaCmd (fechaTimeStamp,hostRemoto,cmd,reconocido) VALUES (?,?,?,?)'
            parametros = (time.time(),rowSesion[0][0],args['input'] + " " + args['realm'],2)
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()

        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

        self.write(session, 'Unknown command [%s]' % (args['input'],))
        self.write(session, 'Input [%s] @%s' % (args['input'], args['realm']))

    def handleTerminalSize(self, session, args):
        ###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo terminalSize Terminal size: %sx%s\n' % (args['width'], args['height']))
        #prueba.close()
        ###DEPURACION

        try:
            conexionBD = dbapi2.connect(self.db)
            cursorInsercion = conexionBD.cursor()	
            cadenaInsercion = 'UPDATE OR IGNORE tablaSesionesOnline SET terminalWidth=?,terminalHeight=? WHERE sesionId=?'
            parametros = (args['width'],args['height'],session)
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()
        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

    def handleClientVersion(self, session, args):
        ###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo clientVersion Client version: [%s]\n' % (args['version'],))
        #prueba.close()
        ###DEPURACION

        try:
            conexionBD = dbapi2.connect(self.db)

            cursorSeleccion = conexionBD.cursor()
            cadenaSeleccion = 'SELECT hostRemoto FROM tablaSesionesOnline WHERE sesionId=?'
            parametros = (session,)
            cursorSeleccion.execute(cadenaSeleccion,parametros)
            rowSesion = cursorSeleccion.fetchall()
            conexionBD.commit()
            cursorSeleccion.close()

            cursorInsercion = conexionBD.cursor()
            cadenaInsercion = 'INSERT OR IGNORE INTO tablaCliente (fechaTimeStamp,hostRemoto,cliente) VALUES (?,?,?)'
            parametros = (time.time(),rowSesion[0][0],args['version'])
            cursorInsercion.execute(cadenaInsercion,parametros)
            conexionBD.commit()
            cursorInsercion.close()

        except Exception,e:
            print '[EXCEPCION]' + str(e)
            return

    def handleFileDownload(self, session, args):
        ###DEPURACION
        #prueba = file('/home/zetsu/salida.txt', 'a')
        #prueba.write('\nModulo fileDownload File download: [%s] -> %s\n' % (args['url'], args['outfile']))
        #prueba.close()
        ###DEPURACION
        pass

# vim: set sw=4 et:
