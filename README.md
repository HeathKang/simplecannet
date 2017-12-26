## simplecannet
### Description
simplecannet is a library to transmit or send messages via TCP method.
Referenced [python-can](https://github.com/hardbyte/python-can).So
 if you want to use more interfaces such as USBcan, Socketcan, you can
 see [python-can](https://github.com/hardbyte/python-can)



### Usage
```python
from simplecannet.client import TcpcanBus
from simplecannent.message import Message

bus = Tcpcanbus(ip="192.168.1.10", port=4001)
msg = Message(arbitration_id=id,
                      data=data,
                      extended_id=False,
                      is_remote_frame=False,
                      )
# send a meassage
# bus.send(msg)  # wait for implement

# receive a meassage
recv_msg = bus.recv()

# reconnect
bus.reconnect()

