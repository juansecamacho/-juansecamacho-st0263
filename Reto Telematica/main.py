import json
import argparse
import threading
from cliente_p2p import ClienteP2P
from p2p_server import app, configurar_servidor, actualizar_peers, start_grpc_server

def cargar_configuracion(ruta_config):
    with open(ruta_config, 'r') as archivo:
        return json.load(archivo)
    
def iniciar_cliente(cliente_p2p):
    cliente_p2p.realizar_bootstrap()

def iniciar_servidor(config, cliente_p2p):
    configurar_servidor(config, cliente_p2p)
    hilo_http = threading.Thread(target=lambda: app.run(host=config['node']['ip'], port=config['node']['port']))
    hilo_http.start()

    # Iniciar el servidor gRPC en un hilo separado
    hilo_grpc = threading.Thread(target=start_grpc_server, args=(config['node']['grpc_port'], config['resources']['shared_directory']))
    hilo_grpc.start()

    hilo_http.join()
    hilo_grpc.join()

def iniciar_nodo(config_file):
    config = cargar_configuracion(config_file)
    
    mi_ip = config['node']['ip']
    mi_puerto = config['node']['port']
    grpc_port = config['node']['grpc_port']
    
    cliente_p2p = ClienteP2P(grpc_port=grpc_port, bootstrap_peers=config['node']['bootstrap_peers'], mi_ip=mi_ip, mi_puerto=mi_puerto)
    
    hilo_servidor = threading.Thread(target=iniciar_servidor, args=(config, cliente_p2p))
    hilo_servidor.start()

    iniciar_cliente(cliente_p2p)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Iniciar un nodo P2P.')
    parser.add_argument('--config', type=str, required=True, help='Ruta al archivo de configuración JSON')

    args = parser.parse_args()

    iniciar_nodo(args.config)
