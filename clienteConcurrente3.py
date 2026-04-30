import socket
import time

# Cliente de prueba 3: envía múltiples mensajes en secuencia
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion_servidor = ('localhost', 10000)
print('[CLIENTE 3] Conectando a servidor...')

try:
    # Conectar al servidor
    sock.connect(direccion_servidor)
    print('[CLIENTE 3] Conectado exitosamente\n')
    
    # Enviar múltiples mensajes en secuencia
    mensajes = [
        b'Primer mensaje',
        b'Segundo mensaje desde C3',
        b'Tercero y final'
    ]
    
    for i, mensaje in enumerate(mensajes, 1):
        print(f'[CLIENTE 3] Enviando mensaje {i}: {mensaje!r}')
        sock.sendall(mensaje)
        
        # Recibir la respuesta del servidor
        datos_recibidos = b''
        while len(datos_recibidos) < len(mensaje):
            datos = sock.recv(16)
            if not datos:
                break
            datos_recibidos += datos
        
        print(f'[CLIENTE 3] Respuesta {i}: {datos_recibidos!r}\n')
        
        # Pequeño delay entre mensajes
        time.sleep(15)

finally:
    print('[CLIENTE 3] Cerrando conexión...')
    sock.close()
    print('[CLIENTE 3] Desconectado')
