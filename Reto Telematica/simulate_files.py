import grpc
import config_pb2 as pb2
import config_pb2_grpc as pb2_grpc

def listar_archivos(peer, grpc_port):
    # Formar la dirección correctamente
    with grpc.insecure_channel(f'{peer}:{grpc_port}') as channel:
        stub = pb2_grpc.FileServiceStub(channel)
        response = stub.ListFiles(pb2.Empty())
        return response.files

peers = [
    '127.0.0.1:5000',  # Nodo 1
    '127.0.0.1:5001',  # Nodo 2
    '127.0.0.1:5002'   # Nodo 3
]


grpc_port = 6000

for peer in peers:
    print(f"Conectando a {peer.split(':')[0]} en el puerto gRPC {grpc_port}...")
    archivos = listar_archivos(peer.split(':')[0], grpc_port)
    print(f"Archivos en {peer.split(':')[0]}:{grpc_port}: {archivos}")
