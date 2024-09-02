from flask import Flask, request, jsonify, send_file
import grpc
from concurrent import futures
from config_pb2_grpc import FileServiceServicer, add_FileServiceServicer_to_server
from config_pb2 import FileListResponse
import os


app = Flask(__name__)

# Variables globales para IP, Puerto, Directorio, y Peers
IP = "0.0.0.0"
PORT = 5000
SHARED_DIRECTORY = "./shared_files"
CLIENTE_P2P = None
PEERS = []

def configurar_servidor(config, cliente_p2p):
    global IP, PORT, SHARED_DIRECTORY, CLIENTE_P2P
    IP = config['node']['ip']
    PORT = config['node']['port']
    SHARED_DIRECTORY = config['resources']['shared_directory']
    CLIENTE_P2P = cliente_p2p
    print(f"Configuración del servidor cargada: Directorio compartido en {SHARED_DIRECTORY}")

def actualizar_peers(nuevos_peers):
    global PEERS
    for peer in nuevos_peers:
        if peer not in PEERS:
            PEERS.append(peer)
    print(f"Peers actualizados: {len(nuevos_peers)} nuevos. Total de peers conocidos: {len(PEERS)}.")

@app.route('/discover', methods=['GET'])
def discover():
    global PEERS
    # Asegurarse de que el nodo incluya su propia dirección en la lista de peers
    self_peer = f"{IP}:{PORT}"
    if self_peer not in PEERS:
        PEERS.append(self_peer)
    
    print(f"Lista de peers conocida en este nodo: {PEERS}")
    return jsonify({"peers": PEERS})

@app.route('/updatePeers', methods=['POST'])
def update_peers():
    nuevos_peers = request.json.get('peers', [])
    if nuevos_peers:
        peers_no_conocidos = [peer for peer in nuevos_peers if peer not in PEERS]
        if peers_no_conocidos:
            print(f"Recibidos {len(peers_no_conocidos)} nuevos peers.")
            actualizar_peers(peers_no_conocidos)
            CLIENTE_P2P.informar_peers(peers_no_conocidos)
        else:
            print("No hay nuevos peers para propagar.")
        return jsonify({"message": "Lista de peers actualizada"}), 200
    return jsonify({"error": "No se proporcionaron peers"}), 400

@app.route('/upload', methods=['POST'])
def upload_file():
    # Simulación de subida de archivo
    file = request.files.get('file')
    if file:
        
        return jsonify({'message': 'El archivo ha sido subido con éxito'}), 200
    else:
        return jsonify({'message': 'No se encontró ningún archivo para subir'}), 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Archivo no encontrado", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

class FileService(FileServiceServicer):
    def __init__(self, shared_directory):
        self.shared_directory = shared_directory

    def ListFiles(self, request, context):
        try:
            # Obtiene la lista de archivos en el directorio compartido
            archivos = os.listdir(self.shared_directory)
            return FileListResponse(files=archivos)
        except Exception as e:
            context.set_details(f'Error al listar archivos: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return FileListResponse()

def start_grpc_server(grpc_port, shared_directory):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service = FileService(shared_directory)
    add_FileServiceServicer_to_server(file_service, server)
    server.add_insecure_port(f'[::]:{grpc_port}')
    print(f"Servidor gRPC iniciado en el puerto {grpc_port}")
    server.start()
    server.wait_for_termination()