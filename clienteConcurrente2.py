import socket
import time

# Cliente de prueba 2: envía un mensaje más largo, con delays para ver concurrencia
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion_servidor = ('localhost', 10000)
print('[CLIENTE 2] Conectando a servidor...')

try:
    # Conectar al servidor
    sock.connect(direccion_servidor)
    print('[CLIENTE 2] Conectado exitosamente')
    
    # Enviar un mensaje más largo
    mensaje = b'Este es un mensaje largo desde Cliente 2 que sera dividido'
    print(f'[CLIENTE 2] Enviando: {mensaje!r}')
    sock.sendall(mensaje)
    
    # Esperar un poco antes de recibir (para simular procesamiento)
    print('[CLIENTE 2] Esperando 50 segundos antes de recibir...')
    time.sleep(50)
    
    print('[CLIENTE 2] Recibiendo respuesta...')
    datos_recibidos = b''
    
    while len(datos_recibidos) < len(mensaje):
        datos = sock.recv(16)
        if not datos:
            break
        datos_recibidos += datos
        print(f'[CLIENTE 2] Recibido fragmento: {datos!r}')
        time.sleep(0.1)  # Pequeño delay entre recepciones
    
    print(f'[CLIENTE 2] Respuesta completa: {datos_recibidos!r}')

finally:
    print('[CLIENTE 2] Cerrando conexión...')
    sock.close()
    print('[CLIENTE 2] Desconectado')
