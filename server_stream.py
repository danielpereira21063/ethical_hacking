import socket
import cv2
import numpy as np

# Configurações de vídeo
WIDTH = 320
HEIGHT = 240

# Configurações de rede
SERVER_HOST = "192.168.0.12"
SERVER_PORT = 5000

# Inicialização do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

# Conexão do cliente
client_socket, client_address = server_socket.accept()

# Leitura dos dados do cliente
while True:
    # Leitura dos dados recebidos
    data = b""
    while True:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    # Decodificação dos dados em um frame de imagem
    image = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Redimensionamento do frame para a resolução correta
    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    # Exibição do frame
    cv2.imshow("Server", frame)

    # Verificação de tecla pressionada para sair
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Encerramento do socket e da janela de exibição
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()