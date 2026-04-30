import socket
import time

# Cliente de prueba 1: envía un mensaje corto, espera respuesta, cierra rápido
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion_servidor = ('localhost', 10000)
print('[CLIENTE 1] Conectando a servidor...')

try:
    # Conectar al servidor
    sock.connect(direccion_servidor)
    print('[CLIENTE 1] Conectado exitosamente')
    
    # Enviar un mensaje simple
    mensaje = b'Hola desde Cliente 1'
    print(f'[CLIENTE 1] Enviando: {mensaje!r}')
    sock.sendall(mensaje)
    
    # Esperar a recibir la respuesta (el servidor hace eco)
    print('[CLIENTE 1] Esperando respuesta...')
    datos_recibidos = b''
    mientras_recibe = 0
    
    while len(datos_recibidos) < len(mensaje):
        datos = sock.recv(16)
        if not datos:
            break
        datos_recibidos += datos
        print(f'[CLIENTE 1] Recibido fragmento: {datos!r}')
    
    print(f'[CLIENTE 1] Respuesta completa: {datos_recibidos!r}')

finally:
    print('[CLIENTE 1] Cerrando conexión...')
    sock.close()
    print('[CLIENTE 1] Desconectado')
