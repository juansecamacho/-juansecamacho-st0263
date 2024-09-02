import time
import requests
import grpc
from config_pb2 import Empty
from config_pb2_grpc import FileServiceStub
from p2p_server import upload_file

class ClienteP2P:
    def __init__(self, grpc_port, bootstrap_peers, mi_ip, mi_puerto, max_reintentos=2, intervalo_reintentos=10):
        self.peers_descubiertos = []  # Lista de peers descubiertos por este nodo
        self.bootstrap_peers = bootstrap_peers  # Peers iniciales para bootstrap
        self.mi_ip = mi_ip  # IP de este nodo
        self.mi_puerto = mi_puerto  # Puerto de este nodo
        self.grpc_port = grpc_port
        self.max_reintentos = max_reintentos  # Número máximo de reintentos de bootstrap
        self.intervalo_reintentos = intervalo_reintentos  # Intervalo entre reintentos

    def realizar_bootstrap(self):
        peers_totales = set()

        for reintento in range(self.max_reintentos):
            for peer in self.bootstrap_peers:
                try:
                    ip, port = peer.split(":")
                    url = f"http://{ip}:{port}/discover"
                    response = requests.get(url)
                    if response.status_code == 200:
                        nuevos_peers = response.json().get('peers', [])
                        peers_totales.update(nuevos_peers)
                        print(f"Conectado a {peer}. Peers descubiertos: {len(nuevos_peers)}")
                    else:
                        print(f"Error al conectarse a {peer}: {response.status_code}")
                except Exception as e:
                    print(f"Error al conectar al peer {peer}: {e}")
            if peers_totales:
                print(f"Bootstrap completado. Peers descubiertos: {len(peers_totales)}")
                return list(peers_totales)
            time.sleep(self.intervalo_reintentos)
        print("No se pudo conectar a ningún peer semilla.")
        return []

    def informar_peers(self, nuevos_peers):
        for peer in self.peers_descubiertos:
            try:
                ip, port = peer.split(":")
                url = f"http://{ip}:{port}/updatePeers"
                response = requests.post(url, json={"peers": nuevos_peers})
                if response.status_code == 200:
                    print(f"Peer {peer} informado exitosamente.")
                else:
                    print(f"Error al informar al peer {peer}: {response.status_code}")
            except Exception as e:
                print(f"Error al conectar con el peer {peer} para actualizar peers: {e}")
        print(f"Nodos informados: {len(nuevos_peers)} nuevos peers distribuidos a {len(self.peers_descubiertos)} peers conocidos.")

    def actualizar_peers(self, nuevos_peers):
        peers_nuevos_descubiertos = []
        for peer in nuevos_peers:
            if peer not in self.peers_descubiertos:
                self.peers_descubiertos.append(peer)
                peers_nuevos_descubiertos.append(peer)
        print(f"\nTabla de peers actualizada en el nodo ({self.mi_ip}:{self.mi_puerto}):")
        for i, peer in enumerate(self.peers_descubiertos, start=1):
            print(f"  Peer {i}: {peer}")
        return peers_nuevos_descubiertos

    def listar_archivos_peer(self, peer):
        ip, port = peer.split(":")
        with grpc.insecure_channel(f'{ip}:{self.grpc_port}') as channel:
            stub = FileServiceStub(channel)
            try:
                response = stub.ListFiles(Empty())
                print(f"Archivos en {peer}: {response.files}")
                return response.files
            except grpc.RpcError as e:
                print(f"Error al listar archivos en {peer}: {e.details()} (Código: {e.code()})")
                return []
            
  
    def upload_file(file_path):
        BASE_URL = "http://127.0.0.1:5000"      
        file_name = file_path.split('/')[-1]
        with open(file_path, 'rb') as file:
            response = requests.post(f"{BASE_URL}/upload/{file_name}", files={'file': file})
        if response.status_code == 200:
            print(f"Archivo '{file_name}' subido exitosamente.")
        else:
            print(f"Error al subir el archivo: {response.status_code} - {response.text}")

# Función para descargar un archivo
def download_file(file_name):
    BASE_URL = "http://127.0.0.1:5000"     
    response = requests.get(f"{BASE_URL}/download/{file_name}", stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Archivo '{file_name}' descargado exitosamente.")
    else:
        print(f"Error al descargar el archivo: {response.status_code} - {response.text}")

    if __name__ == "__main__":
    # Ejemplo de uso
    # Sube un archivo
        upload_file("testfile.txt")

    # Descarga un archivo
        download_file("testfile.txt")