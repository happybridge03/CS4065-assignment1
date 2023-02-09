"""
Assignment 1 
Sean Bridge

Code for Task 1. Webserver implementation.
"""
import socket
import threading
from typing import Any


class WebServer():

    def main():
        port = 6789

        # Create & bind a TCP socket
        with socket.create_server(('', 6789)) as server:
            while (True):
                # Listen for a TCP connection request
                conn, address = server.accept()

                # Construct object to process the HTTP request message
                request = HttpRequest(conn)

                # Create a new thread to process request
                thread = threading.Thread(target=request)

                # Start the thread
                thread.run()


class HttpRequest():

    def __init__(self, conn: socket.socket) -> None:
        self.socket = conn

    # What gets called in the thread
    def __call__(self, *args: Any, **kwds: Any) -> None:
        self.process_request()

    def process_request(self):
        pass


if __name__ == "__main__":
    WebServer.main()
