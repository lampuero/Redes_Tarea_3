# Tarea 3 Redes

## Consideraciones para correr
- Los archivos fueron probados en Python 3.6.5
- Las instrucciones para correr los archivos se mantienen con respecto a las proporcionadas con los archivos originales.
- El nombre de router `REPLACE THIS NAME` es reservado y no debe ser usado dentro de la topología que se use.
- Al crear los routers con el comando `routers = start('topology.json')`, estos intercambiaran mensajes, por lo que se debe esperar hasta que todos los router terminen de imprimir el mensaje `Packet received` y comiencen a imprimir `Broadcasting`.

## Consideraciones para revisar

### En el archivo router.py

- Se agregaron las funciones `init_table` y `_send_new_distance` al final del archivo.
- Se modificaron (agrego código) a las funciones  `__init__` y `_new_packet_received`.
- Se agregan dos variables a cada Router, dos diccionarios que representan las siguientes tablas:
    - Una tabla guarda la distancia a cada router.
    - Una tabla para rutear especificando el puerto por el que el router debe enviar el mensaje.
- Ambas tablas ocupan como llave los nombres de los routers.
- Para calcular la distancia se utilizo la premisa que dos routers conectados directamente por un RouterPort están a distancia 1.
### En el archivo topology.py
- Se modifico (agrego código) a la función `start`.

## Autores

- Luis Ampuero C.
- Vicente Illanes
