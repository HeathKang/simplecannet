# -*- coding: utf-8 -*-
import logging
import socket
from simplecannet.connection import Connection

logger = logging.getLogger(__name__)


class TcpcanBus:
    """CAN bus over a tcp net"""

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.init()

    def init(self):
        """
        init tcp socket
        :param ip: server ip
        :param port: server port
        :return: 
        """
        self.connection = Connection(self.ip, self.port)

    def recv(self, timeout=None):
        """
        recv bus data from tcp server within timeout
        :param timeout: 
        :return: 
        """
        data = self.connection.recv(timeout)
        return data

    def shutdown(self):
        """
        shutdown tcp socket
        :return: 
        """
        self.connection.destroy()

    def reconnect(self):
        """
        reconnect to tcp server
        :return: 
        """
        self.connection.reconnect()
