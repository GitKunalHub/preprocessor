import socket
import time

def wait_for_rabbitmq(host, port, timeout=30):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, int(port)), timeout=2):
                print(f"RabbitMQ is up! host: {host}, port: {port}")
                return
        except Exception:
            if time.time() - start_time > timeout:
                print(f"Timeout waiting for RabbitMQ! host: {host}, port: {port}")
                raise
            print(f"Waiting for RabbitMQ... host: {host}, port: {port}")
            time.sleep(2)