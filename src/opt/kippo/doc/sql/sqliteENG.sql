/*
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
*/

CREATE TABLE "online_sessions_table" (
  "connection_timestamp" FLOAT NOT NULL,
  "session_id" TEXT PRIMARY KEY  NOT NULL  UNIQUE,
  "local_host" TEXT NOT NULL,
  "local_port" INTEGER NOT NULL,
  "remote_host" TEXT NOT NULL,
  "remote_port" INTEGER NOT NULL,
  "terminal_width" INTEGER NOT NULL,
  "terminal_height" INTEGER NOT NULL
);

CREATE TABLE "auth_table" (
  "login_timestamp" FLOAT NOT NULL,
  "remote_host" TEXT NOT NULL,
  "login" TEXT NOT NULL,
  "password" TEXT NOT NULL,
  "result" BOOL NOT NULL
);

CREATE TABLE "command_table" (
  "command_timestamp" FLOAT NOT NULL,
  "remote_host" TEXT NOT NULL,
  "command" TEXT NOT NULL,
  "known" INTEGER NOT NULL
);

CREATE TABLE "client_table" (
  "client_timestamp" FLOAT NOT NULL,
  "remote_host" TEXT NOT NULL,
  "client" TEXT NOT NULL
);
