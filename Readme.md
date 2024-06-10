# Tarea 1

## Instalación

No se usó ningun frakmework de js para esta tarea, por lo que no es necesario instalar nada

## Decisiones

Para el Form para la selección de productos se decidió usar elemento "checkbox" en vez de un "select", pues es más fácil para el usuario la seleccion de multiple frutas sin la necesidad de ponerse muy denso con javascript.

Despues de confirmar el envio no se me ocurrió mejor forma de mostrar el mensaje final de 'Hemos recibido el registro del producto.
 Muchas gracias.' que redirigiendo una nueva página.

 # Tarea 2

 ## instalación 

 correr pip install -r requirements.txt para instalar paquetes necesarios de python, credenciales de mysql están hardcodeados en database/db.py.

 ## decisiones

 no pude visualizar las imagenes usando la ruta guardada en la base de datos por lo que hay una vista en app "display_image(filename)" que entrega un url que permite ver las imagenes. 
 no se guardan distintos tamaños de imagenes, se resizea una sola imagen tal como se hizo para la tarea 1.
 productos: se pueden ingresar, ver en lista y ver detalles.
 pedidos: se pueden ingresar, ver en lista.
vistas de listas estan limitadas a 5 rows definidos en ITEMS_IN_PAGE en app.py, lista están paginadas.

formulario pueden fallar en backend por las mismas validaciones de front y tambien cuando comuna.id, fruta.nombre no existen en BBDD o tipo no es fruta o verdura.