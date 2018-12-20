# Tarea 3 Redes

## Consideraciones para correr
- Los archivos fueron probados en Python 3.6.5
- Las instrucciones para correr los archivos se mantienen con respecto a las proporcionadas con los archivos originales. 
- El nombre de router `REPLACE THIS NAME` es reservado y no debe ser usado dentro de la topología que se use.
- Al crear los routers con el comando `routers = start('topology.json')`, estos intercambiaran mensajes, por lo que se debe esperar hasta que todos los router terminen de imprimir el mensaje `Packet received` y comiencen a imprimir `Broadcasting`.

## Consideraciones para revisar

### En el archivo router.py
- Se agregan dos variables a cada Router, dos diccionarios que representan las siguientes tablas:
 una tabla guarda la distancia a cada router y la otra tabla para rutear especificando el output para cada router.
- Se agregaron las funciones `init_table` y `_send_new_distance` al final del archivo.
- Se modificaron (agrego código) a las funciones  `__init__` y `_new_packet_received`.

### En el archivo topology.py
- Se modifico (agrego código) a la función `start`.