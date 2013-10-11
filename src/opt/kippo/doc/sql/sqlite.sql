CREATE TABLE "tablaSesionesOnline" (
  "fechaTimeStamp" FLOAT NOT NULL,
  "sesionId" TEXT PRIMARY KEY  NOT NULL  UNIQUE,
  "hostLocal" TEXT NOT NULL,
  "puertoLocal" INTEGER NOT NULL,
  "hostRemoto" TEXT NOT NULL,
  "puertoRemoto" INTEGER NOT NULL,
  "terminalWidth" INTEGER NOT NULL,
  "terminalHeight" INTEGER NOT NULL
);

CREATE TABLE "tablaLogin" (
  "fechaTimeStamp" FLOAT NOT NULL,
  "hostRemoto" TEXT NOT NULL,
  "login" TEXT NOT NULL,
  "password" TEXT NOT NULL,
  "resultado" BOOL NOT NULL
);

CREATE TABLE "tablaCmd" (
  "fechaTimeStamp" FLOAT NOT NULL,
  "hostRemoto" TEXT NOT NULL,
  "cmd" TEXT NOT NULL,
  "reconocido" INTEGER NOT NULL
);

CREATE TABLE "tablaCliente" (
  "fechaTimeStamp" FLOAT NOT NULL,
  "hostRemoto" TEXT NOT NULL,
  "cliente" TEXT NOT NULL
);
