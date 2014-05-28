import marshal
import logging

from packets.HandshakePkts import *
from Version import *

class EVESession():

    def __init__(self, connection):
        self.packetHandler = None
        self.connection = connection

    def reset(self):
        self.packetHandler = None
        # TO-DO: Check to see if we are still connected

        print "Called reset"

        version = VersionExchangeServerPkt(EVEVersion.EVEBirthday, 
                                            EVEVersion.MachoNetVersion,
                                            1,# this should be the clients count 
                                            EVEVersion.EVEVersionNumber, 
                                            EVEVersion.EVEBuildVersion,
                                            EVEVersion.EVEProjectVersion)

        packet = version.encode()

        # Send packet to queue
        self.connection.queuePacket(packet)

        self.packetHandler = self.handleVersion
        print repr(self.packetHandler)

        return

    def popPacket(self):
        print "Called popPacket"
        packet = self.connection.dequeuePacket()

        return self.packetHandler(packet)

    def handleVersion(self, packet):
        print "Called handleVersion: \n"
        versionExClient = VersionExchangeClientPkt(packet)

        if not versionExClient:
            logging.critical("Received invalid version exchange!")

        elif self.verifyVersion(versionExClient):
            # All is good - Client is compatible with the server
            # We wait for the command packet now
            self.packetHandler = self.handleCommand

        # Recurse - grab another packet from the queue
        return self.popPacket()
    
    def handleCommand(self, packet):
        # Check to see if it is a tuple
        print "Called handleCommand: \n"
        packet = marshal.loads(packet)
        
        if type(packet) is not tuple:
            logging.critical("Invalid packet during waiting for command (tuple expected) got: %s" & (type(packet)))
        
        # Got queue check command
        elif packet.count == 2:
            cmd = NetCommand_QC(packet)
            
            if not cmd:
                logging.critical("Failed to decode 2-arg command")
            else:
                logging.info("Got Queue Check command.")
                # Respond to the client with the queue position

                # Reset session
                self.reset()
        
        # Got request for the VipKey... Continue with login
        elif packet.count == 3:
            cmd = NetCommand_VK(packet)
            
            if not cmd:
                logging.critical("Failed to decode 3-arg command")
            
            elif self.verifyVipKey(cmd):
                self.packetHandler = self.handleCrypto
        
        return self.popPacket()

    def handleCrypto(self, packet):
        packet = marshal.loads(packet)
        cr = CryptoRequestPacket(packet)

        if not cr:
            logging.critical("Received invalid crypto request!")
        
        elif self.verifyCrypto(cr):
            self.packetHandler = self.handleAuthentication
        
        return self.popPacket()

    def handleAuthentication(self, packet):
        packet = marshal.loads(packet)
        ccp = CryptoChallengePacket(packet)

        if not ccp:
            logging.critical("Received invalid crypto challenge!")
        
        elif self.verifyLogin(ccp):
            self.packetHandler = self.handleFuncResult
        
        return self.popPacket()
    
    def handleFuncResult(self, packet):
        packet = marshal.loads(packet)
        hr = CryptoHandshakeResult(packet)

        if not hr:
            logging.critical("Received invalid crypto handshake!")
        
        elif self.verifyFuncResult(hr):
            self.packetHandler = self.handlePacket
        
        return self.popPacket()
    
    def handlePacket(self, packet):
        packet = marshal.loads(packet)
        
        # We need to implement the standard PyPacket structure
        if not packet:
            logging.critical("Failed to decode packet!")
        else:
            return packet

        return self.popPacket()
    
    # Virtual stuff that needs to be implemented in the Client.py
    def verifyVersion(self, version):
        raise NotImplementedError("Need to implement this!")
    
    def verifyVipKey(self, vipKey):
        raise NotImplementedError("Need to implement this!")
    
    def verifyCrypto(self, crypto):
        raise NotImplementedError("Need to implement this!") 
    
    def verifyLogin(self, cryptoChallenge):
        raise NotImplementedError("Need to implement this!")
    
    def verifyFuncResult(self, handshakeResult):
        raise NotImplementedError("Need to implement this!")
    
    
    
    
    
    
    
    
    
    
    
    