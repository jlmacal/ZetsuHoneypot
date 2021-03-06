#Copyright (C) 2013  Juan Luis Martin Acal
#
#Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#bajo los términos de la Licencia Pública General GNU publicada
#por la Fundación para el Software Libre, ya sea la versión 3
#de la Licencia, o (a su elección) cualquier versión posterior.
#
#Este programa se distribuye con la esperanza de que sea útil, pero
#SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita
#MERCANTIL o de APTITUD PARA UN PROPÓSITO DETERMINADO.
#Consulte los detalles de la Licencia Pública General GNU para obtener
#una información más detallada.
#
#Debería haber recibido una copia de la Licencia Pública General GNU
#junto a este programa.
#En caso contrario, consulte <http://www.gnu.org/licenses/>.
#
#
#                contact:  jlmacal@gmail.com
#

#!/bin/bash
cat /dev/null > /opt/dionaea/var/log/dionaea.log
cat /dev/null > /opt/dionaea/var/log/dionaea-errors.log
cat /dev/null > /opt/dionaea/var/dionaea/downloads.f2b
cat /dev/null > /opt/dionaea/var/dionaea/offers.f2b
cat /dev/null > /tmp/p0f.log
rm -f /opt/kippo/log/kippo.log.*
