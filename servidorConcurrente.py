import socket
import threading
import sys

# ============================================================================
# REQUERIMIENTO 1: MANEJO DE MÚLTIPLES CLIENTES
# ============================================================================
# Utilizamos un contador global para rastrear cuántos clientes están conectados
# y un lock (candado) para sincronizar acceso a ese contador desde múltiples hilos
clientes_activos = 0  # Contador de clientes activos en tiempo real
lock_clientes = threading.Lock()  # Lock para sincronizar acceso al contador


# ============================================================================
# REQUERIMIENTO 2: FUNCIÓN MANEJADORA DE CLIENTES
# ============================================================================
def manejar_cliente(conexion, direccion_cliente):
    """
    Función que atiende a UN cliente específico en un hilo independiente.
    
    Parámetros:
    - conexion: socket conectado al cliente
    - direccion_cliente: tupla (IP, puerto) del cliente remoto
    """
    # Declarar la variable global para poder modificar clientes_activos
    global clientes_activos
    
    # Incrementar el contador de clientes activos de forma segura (thread-safe)
    with lock_clientes:
        clientes_activos += 1
        print(f'\n[CLIENTE CONECTADO] {direccion_cliente} | Clientes activos: {clientes_activos}')
    
    try:
        # Bucle para recibir datos del cliente mientras esté conectado
        while True:
            # Recibir datos en segmentos de 16 bytes del cliente
            datos = conexion.recv(16)
            
            # Si recv() devuelve b'' significa que el cliente cerró la conexión
            if not datos:
                print(f'[CLIENTE DESCONECTADO] {direccion_cliente}')
                break
            
            # Imprimir el mensaje recibido del cliente
            print(f'[MENSAJE RECIBIDO] De {direccion_cliente}: {datos!r}')
            
            # Procesar y responder al cliente (en este caso, hacer eco)
            print(f'[ENVIANDO RESPUESTA] Reenviando {len(datos)} bytes a {direccion_cliente}')
            conexion.sendall(datos)
    
    except Exception as e:
        # Capturar cualquier error durante la comunicación con el cliente
        print(f'[ERROR] Con cliente {direccion_cliente}: {e}')
    
    finally:
        # Decrementar el contador de clientes activos de forma segura
        with lock_clientes:
            clientes_activos -= 1
            print(f'[CLEANUP] {direccion_cliente} eliminado | Clientes activos: {clientes_activos}')
        
        # Cerrar la conexión con el cliente
        conexion.close()


# ============================================================================
# REQUERIMIENTO 3: SERVIDOR CONCURRENTE (BLOQUE PRINCIPAL)
# ============================================================================

if __name__ == '__main__':
    # Crear un socket TCP en IPv4
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permitir reutilizar la dirección incluso si estaba en TIME_WAIT
    # Esto evita el error "Address already in use" después de cerrar el servidor
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Definir la dirección donde escuchará el servidor
    direccion_servidor = ('localhost', 10000)
    
    print(f'[SERVIDOR] Iniciando servidor concurrente en {direccion_servidor[0]} puerto {direccion_servidor[1]}')
    
    # Ligar el socket a la dirección del servidor
    sock.bind(direccion_servidor)
    
    # Poner el socket en modo escucha (backlog=5)
    # backlog=5 significa que hasta 5 conexiones pueden esperar en cola
    sock.listen(5)
    
    print('[SERVIDOR] Escuchando conexiones entrantes...\n')

    # Bucle infinito para aceptar clientes continuamente
    while True:
        # accept() bloquea esperando una conexión entrante
        # Devuelve (socket_conectado, dirección_del_cliente)
        conexion, direccion_cliente = sock.accept()
        
        # ================================================================
        # REQUERIMIENTO 1: CREAR UN HILO INDEPENDIENTE POR CLIENTE
        # ================================================================
        # En lugar de procesar el cliente en este hilo (servidor),
        # creamos un nuevo hilo que ejecute manejar_cliente()
        # Esto permite que el bucle principal vuelva a aceptar otros clientes
        
        # Crear un nuevo hilo con target=manejar_cliente (función a ejecutar)
        # args=(conexion, direccion_cliente) son los parámetros para la función
        hilo_cliente = threading.Thread(
            target=manejar_cliente,
            args=(conexion, direccion_cliente),
            # daemon=True hace que el hilo termine cuando el programa principal termina
            daemon=True
        )
        
        # Iniciar la ejecución del hilo
        hilo_cliente.start()
        
        # El bucle principal continúa inmediatamente para aceptar el siguiente cliente
        # El cliente anterior se atiende en paralelo en su propio hilo
