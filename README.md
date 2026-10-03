# Sistema de Inspección Autónoma y Freno de Emergencia (ROS2 + OpenCV)

Sistema distribuido en ROS2 que integra visión por computadora con el control de un agente móvil simulado (`turtlesim`). Simula un escenario de inspección industrial: un robot patrulla continuamente y ejecuta un freno de emergencia automático al detectar una anomalía visual.

## Arquitectura

Dos nodos independientes, comunicados por tópicos:
[detector_vision] --/alerta_seguridad--> [control_robot] --/turtle1/cmd_vel--> [TurtleSim]


- **`detector_vision`**: simula la captura de frames a 1Hz, procesa la imagen en espacio HSV y detecta la presencia de un objeto rojo mediante segmentación de color (`cv2.inRange` + `cv2.countNonZero`). Publica `PELIGRO: ANOMALIA_DETECTADA` u `OK: NORMAL`.
- **`control_robot`**: suscripto a `/alerta_seguridad`. En estado normal, ejecuta un patrullaje circular. Al recibir una alerta de peligro, anula el movimiento e impone un freno de emergencia inmediato.

## Por qué HSV y no BGR

El espacio HSV separa el matiz (color) del brillo, por lo que la detección de color es robusta frente a cambios de luminosidad, algo que no ocurre filtrando directamente en BGR.

## Cómo correrlo

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run inspeccion_ros detector_vision

# Terminal 3
ros2 run inspeccion_ros control_robot
```

## Stack

ROS2 · Python · OpenCV · NumPy

## Posibles extensiones

- Integración con cámara real vía `image_transport` / `cv_bridge`.
- Detección multi-clase (YOLO) para distintos tipos de anomalías.
- Migración a simulación 3D (Gazebo).