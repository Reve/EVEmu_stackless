import logging
import stackless

from packets.HandshakePkts import *
from common.Marshal import *
from Version import *
from Client import Client

class Connection:

    def __init__(self, clientsocket, address, control):

        self.control = control
        self.m = Marshal()

        # 10 megabytes
        self.PACKET_SIZE_LIMIT = 10 * 1024 * 1024;
        self.entity_list = []

        # Packet queues
        self.inbound_pq = []
        self.outbound_pq = []

        self.clientsocket = clientsocket

        # Handle Receive Messages in one tasklet
        self.network(clientsocket, address)



    def network(self, clientsocket, address):
        logging.info("Client %s:%s connected!" % (address[0], address[1]))

        # Create new client
        client = Client(clientsocket, address, self)
        
        # Add client to entity list
        self.entity_list.append(client)
        '''
        data = ''    
        while 1: #clientsocket.connect:
            data = clientsocket.recv(4096)
            if data == '':
                break

            print "hey"

            print data

            # place received packets in queue
            self.inbound_pq.append(data)

            print len(self.outbound_pq)

            # if we have packets in queue, send them
            if len(self.outbound_pq) > 0:
                to_send = self.outbound_pq.pop(0)
                print to_send
                clientsocket.sendall(to_send)

            #stackless.schedule()
            data = ''
        '''
        # Loop over, connection is broken
        logging.info("Connection lost! Client %s:%s is removed." % (address[0], address[1]))
        self.close(clientsocket)
        #self.entity_list.remove(client)

    def close(self, clientsocket):
        clientsocket.close()

    def queuePacket(self, packet):
        marshaledPacket = self.m.marshal(packet)
        #if clientsocket.connect:
        print repr(packet)
        print repr(marshaledPacket)

        self.clientsocket.send(marshaledPacket, 0)

    def dequeuePacket(self):
        print "dequeu"
        data = self.clientsocket.recv(4096 * 2)
        print repr(data)
       # unmarshaledData = marshal.loads(data)
        #return unmarshaledData


