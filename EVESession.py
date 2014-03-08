import marshal

import EVEVersion
from packets.VersionExchangePkt import VersionExchangePkt


# Handshaking steps
EVE_VERSION_EXCHANGE = 0
EVE_COMMAND = 1 
EVE_CRYPTO = 2
EVE_AUTHENTICATION = 3
EVE_FUNC_RESULT = 4
EVE_PACKET_READING = 5

class EVESession:
    
    def __init__(self):
        pass
    
    def sendVersionExchange(self, userCount):
        ve = VersionExchangePkt(EVEVersion.EVEBirthday, 
                                EVEVersion.MachoNetVersion,
                                userCount,
                                EVEVersion.EVEVersionNumber,
                                EVEVersion.EVEBuildVersion,
                                EVEVersion.EVEProjectVersion)
        vePkt = ve.getVersionAsTuple()
        return marshal.dumps(vePkt)
    
    def handleVersion(self):
        pass
    
    def handleCommand(self):
        pass
    
    def handleCrypto(self):
        pass
    
    def handleAuthentication(self):
        pass
    
    def handleFuncResult(self):
        pass
    
    def handlePacket(self):
        pass