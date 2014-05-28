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

    # --------------------
    # EVESession interface
    # --------------------
    
    def verifyVersion(self, version):
        if version.birthday != EVEVersion.EVEBirthday:
            logging.error("Client[%s]: Client's EVE Birthday differs from server's. "
                             "Should be %s not %s" % (self.address, EVEVersion.EVEBirthday, version.birthday))
            return False

        if version.machoNet != EVEVersion.MachoNetVersion:
            logging.error("Client[%s]: Client's MachoNet version differs from server's."
                             "Should be %s not %s" % (self.address, EVEVersion.MachoNetVersion, version.machoNet))
            return False

        if version.versionNumber != EVEVersion.EVEVersionNumber:
            logging.error("Client[%s]: Client's VersionNumber differs from server's."
                             "Should be %s not %s" % (self.address, EVEVersion.EVEVersionNumber, version.versionNumber))
            return False

        if version.buildVersion != EVEVersion.EVEBuildVersion:
            logging.error("Client[%s]: Client's Build Version differs from server's."
                             "Should be %s not %s" % (self.address, EVEVersion.EVEBuildVersion, version.buildVersion))
            return False

        if version.projVersion != EVEVersion.EVEProjectVersion :
            logging.error("Client[%s]: Client's Project Version differs from server's."
                             "Should be %s not %s" % (self.address, EVEVersion.EVEProjectVersion, version.projVersion))
            return False
        
        return True
    
    def verifyVipKey(self, vipKey):
        # This returns true at the moment
        return True
    
    def verifyCrypto(self, crypto):
        if crypto.keyVersion != "placebo":
            car = CryptoAPIRequestParams(marshal.loads(crypto.keyParams))
            
            if not car:
                logging.error("Client[%s]: Received invalid CryptoAPI request!" % (self.address))
            else:
                logging.error("Client[%s]: Unhandled CryptoAPU request: hashmethod=%s, sessionkeylenth=%s, provider=%s sessionkeymethod=%s" 
                                 % (self.address, car.hashMethod, car.sessionKeyLength, car.provider, car.sessionKeyMethod))
                
            return False
        else:
            logging.debug("Client[%s]: Received Placebo crypto request, accepting." % (self.address))
            
            # send response to client
            response = "OK CC"
            
            return True
    
    def verifyLogin(self, cryptoChallenge):
        return True
    
    def verifyFuncResult(self, handshakeResult):
        return True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    