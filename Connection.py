import logging
import stackless

from packets.HandshakePkts import *
from common.Marshal import *
from Version import *
from Client import Client

class Connection:

    def __init__(self, clientsocket, address, control):

        self.control = control
        self.m = EVEMarshal()

        # 10 megabytes
        self.PACKET_SIZE_LIMIT = 10 * 1024 * 1024;
        self.entity_list = []

        # Packet queues
        self.inbound_pq = []
        self.outbound_pq = []

        self.clientsocket = clientsocket
        self.address = address

        # Handle Receive Messages in one tasklet
        self.network(clientsocket, address)



    def network(self, clientsocket, address):
        logging.info("Client %s:%s connected!" % (address[0], address[1]))

        # Create new client
        client = Client(clientsocket, address, self)
        
        # Add client to entity list
        self.entity_list.append(client)

        # Loop over, connection is broken
        logging.info("Connection lost! Client %s:%s is removed." % (address[0], address[1]))
        self.close(clientsocket)
        #self.entity_list.remove(client)

    def close(self, clientsocket):
        clientsocket.close()

    def queuePacket(self, packet):
        marshaledPacket = self.m.marshal(packet)
        data = pack('<b', 0x7E)
        data += pack('<l', 0)
        data += marshaledPacket

        size = pack('<l', len(data))

        data = size + data
        print('OUTBOUND RAW PACKET', repr(packet))
        print('OUTBOUND MARSHALED PACKET', repr(marshaledPacket))

        self.clientsocket.send(data)

    def dequeuePacket(self):
        size = unpack('<l', self.clientsocket.recv(4))[0]
        header = self.clientsocket.recv(5)
        recv = self.clientsocket.recv(size - 5)
        print('INBOUND RAW PACKET', recv)
        data = self.m.unmarshal(recv)
        print('INBOUND UNMARSHALED PACKET', data)

        return data
