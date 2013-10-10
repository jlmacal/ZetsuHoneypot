/*Copyright (C) 2013  Juan Luis Martin Acal

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

function consultaCelda(nombreTabla,nombrePKey,nombreColumna,valorBuscado)
{
	//alert(valorBuscado);	
	document.formConsultas.consultaPersonalizada.value = "SELECT * FROM " + nombreTabla + " WHERE " + nombreColumna + " = '" + valorBuscado + "' ORDER BY " + nombrePKey + " DESC";
}

function consultaCeldaFecha(nombreTabla,nombrePKey,nombreColumna,fechaAntes,fechaDespues)
{
	//alert(fechaDespues);
	//alert(fechaAntes);
	document.formConsultas.consultaPersonalizada.value = "SELECT * FROM " + nombreTabla + " WHERE " + nombreColumna + " BETWEEN '" + fechaAntes + "' AND '" + fechaDespues + "' ORDER BY " + nombrePKey + " DESC" ;
}

//Funcion que muestra el div en la posicion del mouse
function showdiv(event,texto)
{
	//determina un margen de pixels del div al raton
	margin=5;

	//La variable IE determina si estamos utilizando IE
	var IE = document.all?true:false;
	//Si no utilizamos IE capturamos el evento del mouse
	if (!IE) document.captureEvents(Event.MOUSEMOVE)

	var tempX = 0;
	var tempY = 0;

	if(IE)
	{ //para IE
		tempX = event.clientX + document.body.scrollLeft;
		tempY = event.clientY + document.body.scrollTop;
	}else{ //para netscape
		tempX = event.pageX;
		tempY = event.pageY;
	}
	if (tempX < 0){tempX = 0;}
	if (tempY < 0){tempY = 0;}

	//modificamos el valor del id "posicion" para indicar la posicion del mouse
	//document.getElementById('posicion').innerHTML="PosX = "+tempX+" | PosY = "+tempY;
	document.getElementById('posicion').innerHTML="Campo<br />"+texto+"<br />";
	
	document.getElementById('capaFlotante').style.top = (tempY+margin);
	document.getElementById('capaFlotante').style.left = (tempX+margin);
	document.getElementById('capaFlotante').style.display='block';
	return;
}
