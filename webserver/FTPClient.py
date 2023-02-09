"""
Assignment 1
Sean Bridge

Code for Task 2. FTP Client implementation. 
"""
import socket


class FTPClient:

    def connect(self, username: str, password: str):
        pass

    def disconnect(self):
        pass

    def get_file(self, file_name: str):
        pass

    def send_command(self, command: str, expcted_response: int):
        pass

    def check_response(self, expected_code: int):
        pass

    def extract_data_port(self, response_line: str):
        pass

    def create_local_file(self, data: bytes, file_name: str):
        pass
