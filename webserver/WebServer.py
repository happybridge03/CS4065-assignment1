"""
Assignment 1
Sean Bridge

Code for Task 1. Webserver implementation.
"""
# Modules
import socket
import threading
from FTPClient import FTPClient
from typing import Any, IO

# Constants
CRLF = '\r\n'


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
                thread = threading.Thread(target=request, daemon=True)

                # Start the thread
                thread.run()


class HttpRequest:

    def __init__(self, conn: socket.socket) -> None:
        self.socket = conn

    # What gets called in the thread
    def __call__(self, *args: Any, **kwds: Any) -> None:
        self.process_request()

    def process_request(self):
        """ Processes the request associated with this HttpRequest.

        Messages are in the format of...

        Request = Request-Line
                    *( General-Header
                    | Request-Header
                    | Entity-Header)
                    CRLF
                    [ Entity-Body ]

        Response = Status-Line
                   *( General-Header
                    | Response-Header
                    | Entity-Header)
                   CRLF
                   [ Entity-Body ]

        Each of these sections are terminated by a CRLF charecter.
        """
        # Get the data from the socket
        input = str(self.socket.recv(4096), 'ascii')
        input = input.split(CRLF)
        print("Request:\n------")

        # Grab the request line of the HTTP Request
        request_line: str = input.pop(0)
        print(request_line)

        # Grab the header lines
        header_lines = input[:input.index('')]
        input = input[input.index(''):]
        for header in header_lines:
            print(header)

        # Tokenzie the request line
        reqeust_tokens = request_line.split()

        # Skip the method (should be GET)
        reqeust_tokens.pop(0)

        # Get file name, prepending '.' so its in the local directory
        file_name = "." + reqeust_tokens.pop(0)

        # Open the file
        try:
            file_stream = open(file_name, 'br')
        except BaseException:
            file_stream = None

        # Construct response method
        if file_stream:
            status_line = f"HTTP/1.0 200{CRLF}"
            content_type_line = (f"Content-type: "
                                 f"{self.content_type(file_name)}{CRLF}")
        elif file_name.endswith('.txt'):
            # Is a text file, use FTP
            status_line = f"HTTP/1.0 200{CRLF}"
            content_type_line = (f"Content-type: "
                                 f"{self.content_type(file_name)}{CRLF}")

            # Create an FTPClient
            ftp_client = FTPClient()

            # Connect to FTP Server
            ftp_client.connect('user', 'password')

            # Retreive File
            ftp_client.get_file(file_name)

            # Disconnect from FTP Server
            ftp_client.disconnect()

            # Open the file
            try:
                file_stream = open(file_name, 'br')
            except BaseException:
                file_stream = None
                # File doesn't exist
                status_line = f"HTTP/1.0 404{CRLF}"
                content_type_line = f"Content-type: text/html{CRLF}"
        else:
            # File doesn't exist
            status_line = f"HTTP/1.0 404{CRLF}"
            content_type_line = f"Content-type: text/html{CRLF}"

        response = f"{status_line}{content_type_line}{CRLF}"
        entity_body_bytes = self.entity_body(file_stream)

        # Close the file
        if file_stream is not None:
            file_stream.close()

        # Print Response
        print(f"Response\n------\n{response}")

        # Send the response
        response_bytes = bytes(response, 'ascii')
        self.socket.send(response_bytes + entity_body_bytes)

        # Close the socket
        self.socket.close()

    @staticmethod
    def content_type(file_name: str) -> str:
        file_id = file_name[file_name.rfind('.'):]

        match file_id:
            case (".htm" | ".html" | ".txt"):
                return "text/html"
            case ".gif":
                return 'image/gif'
            case ".jpg":
                return 'image/jpeg'
            case _:
                return "application/octet-stream"

    @staticmethod
    def entity_body(file: IO) -> str | bytes:
        if not file:
            return bytes("<html><head><title>Not Found</title></head>"
                         "<body>Not Found</body></html>", 'ascii')
        else:
            return file.read()


if __name__ == "__main__":
    WebServer.main()
