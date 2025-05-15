import cv2
import mediapipe as mp
import math
import time
import serial

# ==========================
# CONFIGURACIÓN PERSONALIZABLE
# ==========================
EAR_THRESHOLD = 0.25           # Umbral para detectar parpadeo
CONSEC_FRAMES = 3              # Nº de frames consecutivos por parpadeo
ALERTA_TIEMPO_SIN_PARPADEO = 10 # Tiempo en segundos para mostrar alerta

# ==========================
# FUNCIONES
# ==========================

def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def get_ear(landmarks, eye_indices, width, height):
    p0 = (int(landmarks[eye_indices[0]].x * width), int(landmarks[eye_indices[0]].y * height))
    p1 = (int(landmarks[eye_indices[1]].x * width), int(landmarks[eye_indices[1]].y * height))
    p2 = (int(landmarks[eye_indices[2]].x * width), int(landmarks[eye_indices[2]].y * height))
    p3 = (int(landmarks[eye_indices[3]].x * width), int(landmarks[eye_indices[3]].y * height))
    p4 = (int(landmarks[eye_indices[4]].x * width), int(landmarks[eye_indices[4]].y * height))
    p5 = (int(landmarks[eye_indices[5]].x * width), int(landmarks[eye_indices[5]].y * height))

    vertical1 = euclidean_distance(p1, p5)
    vertical2 = euclidean_distance(p2, p4)
    horizontal = euclidean_distance(p0, p3)

    return (vertical1 + vertical2) / (2.0 * horizontal)

# ==========================
# CONFIGURAR MEDIAPIPE
# ==========================

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Índices de puntos para los ojos
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# ==========================
# VARIABLES DE ESTADO
# ==========================

frame_counter = 0
blink_count = 0
ultimo_parpadeo = time.time()
# Puerto y velocidad del ESP32 (ajusta el puerto según tu PC)
ser = serial.Serial('COM4', 115200)  # Cambia 'COM4' si es necesario

# ==========================
# INICIAR CÁMARA
# ==========================

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            left_ear = get_ear(landmarks, LEFT_EYE, width, height)
            right_ear = get_ear(landmarks, RIGHT_EYE, width, height)
            ear_avg = (left_ear + right_ear) / 2.0

            # Verificar si hay parpadeo
            if ear_avg < EAR_THRESHOLD:
                frame_counter += 1
            else:
                if frame_counter >= CONSEC_FRAMES:
                    blink_count += 1
                    ser.write(f"PARPADEOS:{blink_count}\n".encode()) #Muestra conteo en el display I2C
                    print(f"Parpadeo #{blink_count}")
                    ultimo_parpadeo = time.time()
                frame_counter = 0

            # Calcular el tiempo sin parpadeo
            tiempo_sin_parpadear = time.time() - ultimo_parpadeo

            # Color dinámico: azul por defecto, rojo si se excede el umbral
            color_timer = (255, 0, 0) if tiempo_sin_parpadear < ALERTA_TIEMPO_SIN_PARPADEO else (0, 0, 255)

            # Mostrar EAR
            cv2.putText(frame, f"EAR: {ear_avg:.2f}", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            # Mostrar conteo de parpadeos
            cv2.putText(frame, f"Parpadeos: {blink_count}", (30, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Mostrar tiempo sin parpadeo en dos líneas
            cv2.putText(frame, "Tiempo sin", (30, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_timer, 2)
            cv2.putText(frame, f"parpadear: {int(tiempo_sin_parpadear)}s", (30, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_timer, 2)

            # Mostrar alerta si no parpadea por mucho tiempo
            if tiempo_sin_parpadear >= ALERTA_TIEMPO_SIN_PARPADEO:
                ser.write(b"ALERTA\n")
                cv2.putText(frame, "ALERTA: NO HAS PARPADEADO", (30, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Blink Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
