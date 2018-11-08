import marshal
import logging

from struct import pack
from packets.HandshakePkts import *
from Version import *

class EVESession():

    def __init__(self, connection):
        self.packetHandler = None
        self.connection = connection

    def reset(self):
        self.packetHandler = None
        # TO-DO: Check to see if we are still connected
        version = VersionExchangeServerPkt(EVEVersion.EVEBirthday, 
                                            EVEVersion.MachoNetVersion,
                                            1,# this should be the clients count 
                                            EVEVersion.EVEVersionNumber, 
                                            EVEVersion.EVEBuildVersion,
                                            EVEVersion.EVEProjectVersion)
        packet = version.encode()

        # Send packet to queue
        self.connection.queuePacket(packet)

        # assign the first handler in handshake
        self.packetHandler = self.handleVersion

        return

    def popPacket(self):
        print("Called ************************************: %s" % (self.packetHandler.__name__))

        packet = self.connection.dequeuePacket()

        return self.packetHandler(packet)

    def handleVersion(self, packet):
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
        if type(packet) is not tuple:
            logging.critical("Invalid packet during waiting for command (tuple expected) got: %s" & (type(packet)))
        
        # Got queue check command
        elif packet[1] == 'QC':
            cmd = NetCommand_QC(packet)
            
            if not cmd:
                logging.critical("Failed to decode 2-arg command")
            else:
                logging.info("Got Queue Check command.")
                # Respond to the client with the queue position

                # Reset session
                self.reset()
        
        # Got request for the VipKey... Continue with login
        elif packet[1] == 'VK':
            cmd = NetCommand_VK(packet)
            
            if not cmd:
                logging.critical("Failed to decode 3-arg command")
            
            elif self.verifyVipKey(cmd):
                self.packetHandler = self.handleCrypto
        
        return self.popPacket()

    def handleCrypto(self, packet):
        cr = CryptoRequestPacket(packet[0], packet[1])

        if not cr:
            logging.critical("Received invalid crypto request!")
        
        elif self.verifyCrypto(cr):
            self.packetHandler = self.handleAuthentication
        
        return self.popPacket()

    def handleAuthentication(self, packet):
        ccp = CryptoChallengePacket(
            clientChallenge='',
            bootVersion=packet[1]['boot_version'],
            userAffiliateID=packet[1]['user_affiliateid'],
            bootRegion=packet[1]['boot_region'],
            machoVersion=packet[1]['macho_version'],
            bootCodename=packet[1]['boot_codename'],
            userPasswordHash=packet[1]['user_password_hash'],
            userPassword=packet[1]['user_password'],
            bootBuild=packet[1]['boot_build'],
            userName='e',
            userLanguageID='en'
        )

        if not ccp:
            logging.critical("Received invalid crypto challenge!")
        
        elif self.verifyLogin(ccp):
            self.packetHandler = self.handleFuncResult
        
        return self.popPacket()
    
    def handleFuncResult(self, packet):
        hr = CryptoHandshakeResult()

        if not hr:
            logging.critical("Received invalid crypto handshake!")
        
        elif self.verifyFuncResult(hr):
            self.packetHandler = self.handlePacket
        
        return self.popPacket()
    
    def handlePacket(self, packet):        
        # We need to implement the standard PyPacket structure
        if not packet:
            logging.critical("Failed to decode packet!")
            self.connection.queuePacket(None)
        else:
            return packet

        return self.popPacket()
    
    # --------------------
    # EVESession handshake
    # --------------------
    
    def verifyVersion(self, version):
        if version.birthday != EVEVersion.EVEBirthday:
            logging.error("Client[%s]: Client's EVE Birthday differs from server's. "
                             "Should be %s not %s" % (self.connection.address, EVEVersion.EVEBirthday, version.birthday))
            return False

        if version.machoNet != EVEVersion.MachoNetVersion:
            logging.error("Client[%s]: Client's MachoNet version differs from server's."
                             "Should be %s not %s" % (self.connection.address, EVEVersion.MachoNetVersion, version.machoNet))
            return False

        if version.versionNumber != EVEVersion.EVEVersionNumber:
            logging.error("Client[%s]: Client's VersionNumber differs from server's."
                             "Should be %s not %s" % (self.connection.address, EVEVersion.EVEVersionNumber, version.versionNumber))
            return False

        if version.buildVersion != EVEVersion.EVEBuildVersion:
            logging.error("Client[%s]: Client's Build Version differs from server's."
                             "Should be %s not %s" % (self.connection.address, EVEVersion.EVEBuildVersion, version.buildVersion))
            return False

        if version.projVersion != EVEVersion.EVEProjectVersion :
            logging.error("Client[%s]: Client's Project Version differs from server's."
                             "Should be %s not %s" % (self.connection.address, EVEVersion.EVEProjectVersion, version.projVersion))
            return False
        
        return True
    
    def verifyVipKey(self, vipKey):
        # This returns true at the moment
        return True
    
    def verifyCrypto(self, crypto):
        if crypto.keyVersion != "placebo":
            car = CryptoAPIRequestParams(crypto.keyParams)
            
            if not car:
                logging.error("Client[%s]: Received invalid CryptoAPI request!" % (self.connection.address))
            else:
                logging.error("Client[%s]: Unhandled CryptoAPI request: hashmethod=%s, sessionkeylenth=%s, provider=%s sessionkeymethod=%s" 
                                 % (self.connection.address, car.hashMethod, car.sessionKeyLength, car.provider, car.sessionKeyMethod))
                
            return False
        else:
            logging.debug("Client: Received Placebo crypto request, accepting.")
            
            # send response to client
            response = "OK CC"
            self.connection.queuePacket(response)
            return True
    
    def verifyLogin(self, cryptoChallenge):
        self.connection.queuePacket((2))
        # some other stuff to send to client here
        srvc = CryptoServerHandshake()
        srvc.serverChallenge = ""
        srvc.funcMarshaledCode = "None"
        srvc.verification = False
        srvc.clusterUserCount = 1
        srvc.proxyNodeID = 0xFFAA
        srvc.userLogonQueuePosition = 0
        srvc.challengeResponseHash = "55087"
        srvc.imageServerURL = "localhost:5000"
        srvc.machoVersion = EVEVersion.MachoNetVersion
        srvc.bootVersion = EVEVersion.EVEVersionNumber
        srvc.bootBuild = EVEVersion.EVEBuildVersion
        srvc.bootCodename = EVEVersion.EVEProjectCodename
        srvc.bootRegion = EVEVersion.EVEProjectRegion

        rsp = srvc.encode()
        self.connection.queuePacket(rsp)

        return True
    
    def verifyFuncResult(self, handshakeResult):
        hrack = CryptoHandshakeResultAck()
        hrack.role = 5003499186008621056
        hrack.userID = 1
        hrack.userType = 1
        hrack.inDetention = None
        hrack.clientHash = None
        hrack.liveUpdates = None
        hrack.languageID = 'en'
        hrack.maxSessionTime = None

        res = hrack.encode()
        self.connection.queuePacket(res)

        return True
