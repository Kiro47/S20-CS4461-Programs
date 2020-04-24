#!/usr/bin/python3

import logging
import socket
import threading
from .utils import is_IPV4

class RoutingServer(object):

    """
    """

    def __init__(self, listening_range:str, listening_port:int):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.debug("Init for routing server")
        self.verify_args(listening_range, listening_port) # Let exceptions rise up
        # Start server
        self.server_runner(listening_range, listening_port)

    def verify_args(self, listening_range:str, listener_port:int):
        """
        Verify initialization arguments for the server are valid

        :listening_range: IPV4 to listen to connections from
        :listener_port: Port number to listen to connections from

        :raise: ValueError when a value is not valid
        """
        # Verify listening_range
        if listening_range == "localhost" or is_IPV4(listening_range):
            pass
        else:
            raise ValueError("Invalid listening range: [{}]".format(listening_range))
        # Verify listener_port
        if isinstance(listener_port, int):
            pass
        else:
            raise ValueError("Invalid listener port: [{}]".format(listener_port))
        return

    def server_runner(self, listening_range:str, listening_port:int):
        """
        Routing Listening instance

        :listening_range: IPV4 to listen to traffic from
        :listening_port: Port to listen to traffic on
        """
        self.logging.info("Starting server listener for {listening_range} on port {listening_port}".format(
            listening_range=listening_range, listening_port=listening_port))
        sockets = list()
        # New sockets listener
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((listening_range, listening_port))
        sock.listen(20)

        # Listening loop
        try:
            while True:
                client_sock, client_addr = sock.accept()
                self.logging.info("Accepting connection from [{}]".format(client_addr))
                sockets.append(client_sock)
                client_thread = threading.Thread(target=self.client_listener, args=(client_sock, client_addr))
                client_thread.start()
        except KeyboardInterrupt as keeb_exception:
            self.logging.info("Shutting down server")
            # Close all sockets and clean up
            self.logging.debug("Closing sockets...")
            for active_socket in sockets:
                if active_socket:
                    active_socket.close()
            sock.close()
            return
        except Exception as exception:
            self.logging.exception("Exception during main listener loop")
            # Close all sockets and clean up
            self.logging.debug("Closing sockets...")
            for active_socket in sockets:
                if active_socket:
                    active_socket.close()
            sock.close()
            return
        return

    def client_listener(self, client_sock, client_addr):
        """
        Client Listener/interactions

        :sock: Client socket
        :host Hostname of the cliet
        """
        sock.send(bytes("", "utf-8")) # TODO: send "Connection established" message

        actions = Actions()
        data = ""

        while True:
            # Wait on recv data
            data += sock.recv(1024).decode("utf-8")
            if not data:
                break
            self.logging.debug("Host [{}], msg: [{}]".format(hostname, data.rstrip()))
#            data = data.rstrip().split("",4)