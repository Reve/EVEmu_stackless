

class VersionExchangePkt:
    
    def __init__(self, birthday, machoNet, userCount, versionNumber, buildVersion, projVersion):
        self.birthday = birthday
        self.machoNet = machoNet
        self.userCount = userCount
        self.versionNumber = versionNumber
        self.buildVersion = buildVersion
        self.projVersion = projVersion
        
    def getVersionAsTuple(self):
        return (
                self.birthday,
                self.machoNet,
                self.userCount,
                self.versionNumber,
                self.buildVersion,
                self.projVersion
            )