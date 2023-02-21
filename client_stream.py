import socket
import cv2
import numpy as np

# Configurações de vídeo
WIDTH = 640
HEIGHT = 480
FPS = 10

# Configurações de rede
SERVER_HOST = "192.168.0.12"
SERVER_PORT = 5000

# Conexão com o servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

while True:
    # Leitura de um frame da câmera
    ret, frame = cap.read()

    # Redimensionamento do frame para menor resolução
    frame = cv2.resize(frame, (int(WIDTH/2), int(HEIGHT/2)))

    # Codificação do frame em JPEG
    _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    data = buffer.tobytes()

    # Envio dos dados do frame para o servidor
    try:
        client_socket.sendall(data)
    except:
        client_socket.close()
        break

# Encerramento da captura de vídeo e do socket
cap.release()
client_socket.close()