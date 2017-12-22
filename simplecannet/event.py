# -*- coding: utf-8 -*-
import struct

from simplecannet.message import Message


class Event:
    """"""
    _STRUCT = struct.Struct('>Bi8s')
    _EXT_FLAG = 0x80
    _REMOTE_FRAME_FLAG = 0x40
    _ERROR_FRAME_FLAG = 0x40

    def __init__(self, msg):
        """
        :param can.Message msg:
            A Message object.
        """
        #: A :class:`can.Message` instance.
        self.msg = msg

    def encode(self):
        """
        package data like this
        flags | id  | data
        --------------------
        1     | 4  |  8
        :return: 
        """
        flags = 0
        length = len(self.msg.data)
        if self.msg.id_type:
            flags |= self._EXT_FLAG
        if self.msg.is_remote_frame:
            flags |= self._REMOTE_FRAME_FLAG
        if self.msg.is_error_frame:
            flags |= self._ERROR_FRAME_FLAG

        flags |= length
        buf = self._STRUCT.pack(flags,
                                self.msg.arbitration_id,
                                bytes(self.msg.data))
        return buf

    @classmethod
    def from_buffer(cls, buf):
        try:
            flags, arb_id, data = cls._STRUCT.unpack_from(buf)
            dlc = flags & 0x0f
            timestamp = 0
        except struct.error:
            raise NeedMoreDataError()

        msg = Message(timestamp=timestamp,
                          arbitration_id=arb_id,
                          extended_id=bool(flags & cls._EXT_FLAG),
                          is_remote_frame=bool(flags & cls._REMOTE_FRAME_FLAG),
                          is_error_frame=bool(flags & cls._ERROR_FRAME_FLAG),
                          dlc=dlc,
                          data=data[:dlc])
        return cls(msg)

    def __len__(self):
        return self._STRUCT.size
