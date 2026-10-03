import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class ControlRobotNode(Node):
    def __init__(self):
        super().__init__('control_robot')
        
        self.subscription = self.create_subscription(
            String,
            '/alerta_seguridad',
            self.alerta_callback,
            10)
        
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.2, self.mover_robot)
        self.estado_alerta = "OK: NORMAL"

    def alerta_callback(self, msg):
        self.estado_alerta = msg.data

    def mover_robot(self):
        vel = Twist()
        
        if "PELIGRO" in self.estado_alerta:
            vel.linear.x = 0.0
            vel.angular.z = 0.0
            self.get_logger().error('FRENO DE EMERGENCIA: Anomalía detectada por OpenCV. Robot detenido.')
        else:
            vel.linear.x = 1.0
            vel.angular.z = 0.5
            self.get_logger().info('Patrullaje normal en curso...')

        self.cmd_vel_pub.publish(vel)

def main(args=None):
    rclpy.init(args=args)
    node = ControlRobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()