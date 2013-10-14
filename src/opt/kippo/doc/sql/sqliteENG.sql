/*
Copyright (C) 2013  Juan Luis Martin Acal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
