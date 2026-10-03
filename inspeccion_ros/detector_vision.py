import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
import numpy as np

class DetectorVisionNode(Node):
    def __init__(self):
        super().__init__('detector_vision')
        self.publisher_ = self.create_publisher(String, '/alerta_seguridad', 10)
        self.timer = self.create_timer(1.0, self.procesar_imagen_simulada)
        self.contador = 0

    def procesar_imagen_simulada(self):
        imagen = np.zeros((300, 300, 3), dtype=np.uint8)
        
        self.contador += 1
        if 5 <= self.contador <= 10:
            cv2.circle(imagen, (150, 150), 40, (0, 0, 255), -1)
        elif self.contador > 15:
            self.contador = 0

        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        rango_rojo_bajo = np.array([0, 120, 70])
        rango_rojo_alto = np.array([10, 255, 255])
        mascara = cv2.inRange(hsv, rango_rojo_bajo, rango_rojo_alto)

        pixeles_rojos = cv2.countNonZero(mascara)
        
        msg = String()
        if pixeles_rojos > 0:
            msg.data = "PELIGRO: ANOMALIA_DETECTADA"
            self.get_logger().warn('OpenCV: ¡Objeto rojo/anomalía detectado!')
        else:
            msg.data = "OK: NORMAL"
            self.get_logger().info('OpenCV: Estado normal en planta...')

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = DetectorVisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()