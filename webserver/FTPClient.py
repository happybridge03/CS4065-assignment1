"""
Assignment 1
Sean Bridge

Code for Task 2. FTP Client implementation.
"""
import socket
import re
import os


class FTPClient:
    CRLF = "\r\n"
    SERVER_PORT = 21
    HOST = "localhost"

    def __init__(self) -> None:
        self._DEBUG = False
        self.control_socket = socket.socket()
        self.current_response = ""

    def connect(self, username: str, password: str):
        try:
            # Establish the control socket
            self.control_socket = socket.create_connection(
                ('', FTPClient.SERVER_PORT))
            self.current_response = str(
                self.control_socket.recv(4096), "ascii")

            # Check if the initial connection response code is ok
            if (self.check_response(expected_code=220)):
                print("Succesfully connected to the FTP server")

            # Send user name and password to the ftp server
            self.send_command(f"USER {username}", 331)
            self.send_command(f"PASS {password}", 230)

        except socket.herror as ex:
            print(f"Unknown Host Exception : {ex}")
        except OSError as ex:
            print(f"OS or IO Error Exception: {ex}")

    def disconnect(self):
        try:
            self.control_socket.close()
        except OSError as err:
            print("OS or IO error when disconnecting", err)

    def get_file(self, file_name: str):
        data_port = 0
        try:
            # Change to current (root) directory first
            self.send_command("CWD /", 250)

            # Set to passive mode and retrieve the data port number from
            #  response
            current_response = self.send_command("PASV", 227)
            data_port = self.extract_data_port(current_response)

            # Connect to the data port
            data_socket = socket.create_connection(('', data_port))

            # Download file from ftp server
            self.send_command(f"RETR {file_name}", 150)
            with data_socket.makefile('rb') as data_reader:
                file_data = data_reader.read()

            # Check if the transfer was succesful
            self.send_command(f"STAT {file_name}", 226)

            # Write data to local file
            self.create_local_file(file_data, file_name)

        except socket.herror as ex:
            print(f"Unknown Host Exception: {ex}")
        except OSError as ex:
            print(f"OS or IO Error Exception: {ex}")

    def send_command(self, command: str, expcted_response: int):

        response = ""
        # Send command to FTP Server. Pad CRLF and enocde before sending
        self.control_socket.sendall(
            f"{command}{FTPClient.CRLF}".encode("ascii"))

        # Get response from server
        response = str(self.control_socket.recv(4096), 'ascii')
        if self._DEBUG:
            print(f"Current FTP response {response}")

        # Check validity of response
        if not response.startswith(str(expcted_response)):
            raise OSError(f"Bad response {response}")

        return response

    def check_response(self, expected_code: int):
        response_status = True
        try:
            if self._DEBUG:
                print("Current FTP Response", self.current_response)
            if not self.current_response.startswith(str(expected_code)):
                response_status = False
                raise OSError("Bad response on send_command",
                              self.current_response)
        except OSError as err:
            print("OS or IO error on send_command", err)

        return response_status

    def extract_data_port(self, response_line: str):
        # Regex to capture everything inside parentheses
        regex_pattern = re.compile(r"\((.*?)\)")
        data_ports_string = re.findall(regex_pattern, response_line)[0]
        p1, p2 = data_ports_string.split(",")[4:]
        data_port = int(p1) * 2**8 + int(p2)
        if self._DEBUG:
            print(f"Port integers: {p1}, {p2} --> Data port: {data_port}")
        return data_port

    def create_local_file(self, data: bytes, file_name: str):
        try:
            with open(os.path.join(os.getcwd(), file_name), mode="wb") as f:
                f.write(data)
        except Exception as err:
            print("Error during create_local_file", err)


def main():
    ftp = FTPClient()
    ftp.connect("user", "password")
    ftp.get_file("ftp_test.txt")
    ftp.disconnect()


if __name__ == "__main__":
    main()
