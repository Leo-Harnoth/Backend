"""Dünne ROS-Hülle: zwei Services, die preferences_db aufrufen."""
import rclpy
from rclpy.node import Node
from assistant_interfaces.srv import GetPreferences, SetPreferences
from assistant_backend import preferences_db as db


class AssistantBackend(Node):
    def __init__(self):
        super().__init__('assistant_backend')
        self.create_service(GetPreferences, '/assistant/get_preferences', self.on_get)
        self.create_service(SetPreferences, '/assistant/set_preferences', self.on_set)
        self.get_logger().info('assistant_backend bereit')

    def on_get(self, request, response):
        response.language = db.get_language(request.user_id)
        return response

    def on_set(self, request, response):
        try:
            db.set_language(request.user_id, request.language)
            response.success, response.message = True, 'Gespeichert'
            self.get_logger().info(f'user {request.user_id}: Sprache = {request.language}')
        except ValueError as e:
            response.success, response.message = False, str(e)
        return response


def main():
    rclpy.init()
    rclpy.spin(AssistantBackend())


if __name__ == '__main__':
    main()
