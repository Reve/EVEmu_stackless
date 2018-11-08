import stackless
import logging
import marshal
import Version

from Session import *
from packets.HandshakePkts import CryptoAPIRequestParams

class Client(EVESession):

    # Grab connection and services for later use
    def __init__(self, clietnsock, address, connection):
        self.clietnsock = clietnsock
        self.connection = connection
        self.address = address
        self.session = EVESession(connection)

        # Start handshake
        self.session.reset()

        self.processNet()
        #stackless.tasklet(self.process)
        
    # Here we pop packets from the queue and we handle them
    def processNet(self):
        while self.clietnsock.connect:
            self.session.popPacket()

    # These functions get updated frequently
    def process(self):
        pass
