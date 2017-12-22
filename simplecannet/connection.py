# -*- coding: utf-8 -*-
import socket
import logging
import time
from simplecannet.event import Event
from simplecannet.message import Message


logger = logging.getLogger(__name__)


class Connection:

    HEART_BEAT = bytes([0xaa,0x00, 0xff, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x55])

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.init()

    def init(self):
        """
        init tcp socket
        :return: 
        """
        try:
            self.socket = socket.create_connection((self.ip, self.port))
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.socket.settimeout(10)

        except Exception as e:
            raise e

    def _recv(self, length=13):
        """
        recv tcp data from server
        :param length: data length 
        :return: 
        """
        try:
            data = self.socket.recv(length)
            return data
        except (InterruptedError, socket.timeout) as e:
            # raise e("Tcp connnection interrupted, please check connection and reconnect")
            self.reconnect()

    def _convert(self, data):
        """
        convert tcp data to can bus event
        :param data: 
        :return: can bus event 
        """
        if data == self.HEART_BEAT:
            return None
        else:
            event = Event.from_buffer(data) # init a Event
        return event.msg

    def recv(self, timeout=None):
        """
        recv can bus data
        :param timeout: 
        :return: 
        """
        data = self._recv()
        data_handle = self._convert(data)

        return data_handle

    def destroy(self):
        """
        destroy tcp socket
        :return: 
        """
        self.socket.close()
        logger.debug("Destroyed tcp socket")

    def reconnect(self):
        """
        reconnect to tcp server
        :return: 
        """
        self.destroy()
        self.init()



