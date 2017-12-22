# -*- coding: utf-8 -*-

from simplecannet import client
import traceback
import cantools
from pprint import pprint
import struct
import sys
import logging

log = logging.getLogger("cannet")


def main():
    db = cantools.db.load_file("avl.dbc")
    print(db.messages)
    bus = client.TcpcanBus("192.168.1.10", 4001)

    try:
        # bus.send(msg)
        # print("Message sent on{}".format(bus.channel_info))
        while True:
            try:
                data = bus.recv()
                print(data)
                if data:
                    recv_msg = db.decode_message(data.arbitration_id, data.data)
                    # print(recv_msg)

                    for k, v in recv_msg.items():
                        print({k: int_to_float(v)})

                    print("Is remote frame: {}".format(data.is_remote_frame))
                    print("Is extended frame: {}".format(data.is_extended_id))
            except Exception as e:
                print(e)
                traceback.print_exc()
                bus.reconnect()

    except Exception as e:
        traceback.print_exc()
        print(e)


def int_to_float(data):
    print(data)
    ba = struct.pack("L", int(data * 1000))
    d = struct.unpack("l", ba)[0] / 1000
    return d


if __name__ == "__main__":
    main()
