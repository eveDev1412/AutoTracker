import cv2
import numpy as np
from sklearn.cluster import KMeans
import tkinter as tk
from tkinter import simpledialog

# Configura la ventana de tkinter
ROOT = tk.Tk()
ROOT.withdraw()

# Pide al usuario que ingrese los datos de la cámara
camera_type = simpledialog.askstring(title="Camera Type", prompt="Enter 'local' for local camera or 'ip' for IP camera:")

# Configurar la captura de video según los datos ingresados por el usuario
if camera_type.lower() == 'local':
    camera_number = simpledialog.askinteger(title="ID Camera", prompt="Which camera do you want to enable? (Default = 0)")
    # Conectar a la cámara local
    cap = cv2.VideoCapture(camera_number)
elif camera_type.lower() == 'ip':
    ip_address = simpledialog.askstring(title="IP Camera", prompt="Enter IP Address of the device:")
    port = simpledialog.askstring(title="Port", prompt="Enter Port number (Default = 8080):")
    # Conectar a la cámara IP
    cap = cv2.VideoCapture(f'http://{ip_address}:{port}/video')
else:
    print("Invalid camera type selected. Please enter 'local' or 'ip'.")

def detect_dominant_color(img):
    # Convertir la imagen a espacio de color RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Redimensionar la imagen a una matriz 1D de píxeles RGB
    pixels = img_rgb.reshape((-1, 3))
    
    # Definir el número de colores a extraer
    num_colors = 5
    
    # Ejecutar el algoritmo de agrupamiento KMeans para extraer los colores dominantes
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    
    # Encontrar el índice del color más dominante 
    dominant_color_index = np.argmax(np.bincount(kmeans.labels_))
    
    # Obtener el color más dominante
    dominant_color = kmeans.cluster_centers_[dominant_color_index].astype(int)
    
    return dominant_color

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # Detectar el color dominante en la imagen
        dominant_color = detect_dominant_color(frame)

        # Mostrar el color dominante en la pantalla
        color_text = f'Dominant Color: RGB({dominant_color[0]}, {dominant_color[1]}, {dominant_color[2]})'
        color_red = int(dominant_color[0])
        color_green = int(dominant_color[1])
        color_blue = int(dominant_color[2])
    
        cv2.putText(frame, color_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (color_blue, color_green, color_red), 2)

        cv2.imshow('Dominant Color Detection', cv2.resize(frame, (400,200)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
