# Servidor Concurrente TCP

## Descripción

Este trabajo implementa un servidor TCP concurrente en Python capaz de atender varios clientes al mismo tiempo usando hilos. Cada nueva conexión se despacha a un hilo independiente para que el servidor principal siga aceptando conexiones sin quedar bloqueado en la recepción de datos.

## Archivos de esta carpeta

- [servidorConcurrente.py](servidorConcurrente.py): servidor principal concurrente.
- [clienteConcurrente1.py](clienteConcurrente1.py): cliente de prueba corto.
- [clienteConcurrente2.py](clienteConcurrente2.py): cliente de prueba con espera para observar concurrencia.
- [clienteConcurrente3.py](clienteConcurrente3.py): cliente de prueba que envía varios mensajes.

## Qué hace cada archivo

### servidorConcurrente.py

- Abre un socket TCP en `localhost:10000`.
- Escucha conexiones entrantes.
- Crea un hilo por cada cliente aceptado.
- Atiende cada cliente con una función dedicada.
- Imprime cliente conectado, mensajes recibidos, cliente desconectado y número de clientes activos.

### clienteConcurrente1.py

- Se conecta al servidor.
- Envía un mensaje corto.
- Recibe la respuesta del servidor y cierra la conexión.

### clienteConcurrente2.py

- Se conecta al servidor.
- Envía un mensaje más largo.
- Espera un 50seg antes de recibir para facilitar la observación de concurrencia.

### clienteConcurrente3.py

- Se conecta al servidor.
- Envía varios mensajes dentro de la misma conexión.
- Recibe la respuesta de cada mensaje.

## Cómo probarlo

1. Inicia el servidor ejecutando [servidorConcurrente.py](servidorConcurrente.py).
2. Abre dos o más terminales y ejecuta al mismo tiempo [clienteConcurrente1.py](clienteConcurrente1.py), [clienteConcurrente2.py](clienteConcurrente2.py) y [clienteConcurrente3.py](clienteConcurrente3.py).
3. Observa la consola del servidor: deben aparecer varias conexiones atendidas en paralelo y el contador de clientes activos debe cambiar conforme conectan y desconectan.

## Qué deberías observar

- Más de un cliente conectado al mismo tiempo.
- Mensajes recibidos desde clientes distintos.
- El servidor sigue aceptando conexiones mientras otros clientes siguen activos.
- El número de clientes activos sube y baja según el estado de cada conexión.

## Idea principal

La diferencia importante con un servidor secuencial es que aquí cada cliente no se atiende dentro del bucle principal, sino en un hilo separado. Eso permite que el servidor continúe aceptando nuevas conexiones mientras otros clientes siguen siendo procesados.

