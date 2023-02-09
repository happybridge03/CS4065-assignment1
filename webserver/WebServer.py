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
        try:
            self.process_request()
        except Exception as e:
            print(e)

    def process_request(self):
        """ Processes the request associated with this HttpRequest.

        Messages are in the format of...

        Request = Request-Line
                    *( General-Header
                    | Request-Header
                    | Entity-Header)
                    CRLF
                    [ Entity-Body ]

        Each of these sections are terminated by a CRLF charecter.
        """
        # Get the data from the socket
        input = str(self.socket.recv(4096), 'ascii')
        input = input.split('\r\n')

        # Grab the request line of the HTTP Request
        request_line: str = input.pop(0)
        print(request_line)

        # Grab the header lines
        header_lines = input[:input.index('')]
        input = input[input.index(''):]
        for header in header_lines:
            print(header)

        # Close socket
        self.socket.close()


if __name__ == "__main__":
    WebServer.main()
