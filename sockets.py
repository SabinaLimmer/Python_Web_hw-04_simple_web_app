import json
import socket
from datetime import datetime

class SocketServer:
    def __init__(self):
        self.server_address = ('localhost', 5000)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.server_address)
        self.message_list = []

    def run_socket_server(self):
        while True:
            data, _ = self.socket.recvfrom(1024)
            data_dict = json.loads(data.decode())
            self.process_message(data_dict)

    def process_message(self, data_dict):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        message = {
            timestamp: data_dict
        }
        self.message_list.append(message)
        self.save_to_file()

    def save_to_file(self):
        with open('storage/data.json', 'w') as file:
            json.dump(self.message_list, file, indent=2)

