
# first packet sent to the client to make sure we are talking with the ritght client
class VersionExchangeServerPkt:
    
    def __init__(self, birthday, machoNet, userCount, versionNumber, buildVersion, projVersion):
        self.birthday = birthday
        self.machoNet = machoNet
        self.userCount = userCount
        self.versionNumber = versionNumber
        self.buildVersion = buildVersion
        self.projVersion = projVersion
        
    def getPacket(self):
        return (
            self.birthday,
            self.machoNet,
            self.userCount,
            self.versionNumber,
            self.buildVersion,
            self.projVersion,
            None                # update_info
            )


class VersionExchangeClientPkt:
    
    def __init__(self, birthday, machoNet, userCount, versionNumber, buildVersion, projVersion):
        self.birthday = birthday
        self.machoNet = machoNet
        self.userCount = userCount
        self.versionNumber = versionNumber
        self.buildVersion = buildVersion
        self.projVersion = projVersion
        
    def getPacket(self):
        return (
            self.birthday,
            self.machoNet,
            self.userCount,
            self.versionNumber,
            self.buildVersion,
            self.projVersion
            )

# This packet places client in connection queue and sends queue position
class NetCommand_QC:

    def __init__(self, queuePosition):
        self.queuePosition = queuePosition

    def getPacket(self):
        return (None, self.queuePosition)


class NetCommand_VK:

    def __init__(self, vipKey):
        self.vipKey = vipKey

    def getPacket(self):
        return (None, self.vipKey)

class CryptoRequestPacket:

    def __init__(self, keyVersion, keyParams):
        self.keyVersion = keyVersion
        self.keyParams = keyParams

    def getPacket(self):
        return (self.keyVersion, self.keyParams)

class CryptoAPIRequestParams:

    def __init__(self, sessionKey, hashMethod, sessionKeyLength, provider, sessionKeyMethod):
        self.sessionKey = sessionKey
        self.hashMethod = hashMethod
        self.sessionKeyLength = sessionKeyLength
        self.provider = provider
        self.sessionKeyMethod = sessionKeyMethod

    def getTuple(self):
        return ({
            'crypting_sessionkey': self.sessionKey,
            'signing_hashmethod': self.hashMethod,
            'crypting_sessionkeylength': self.sessionKeyLength},
            'crypting_securityprovidertype': self.provider},
            'crypting_sessionkeymethod': self.sessionKeyMethod
            })

class CryptoChallengePacket:

    def __init__(self, clientChallenge, machoVersion, bootVersion, 
        bootBuild, bootCodename, bootRegion, userName, 
        userPassword, userPasswordHash, userLanguageID, userAffiliateID):
    self.clientChallenge = clientChallenge
    self.machoVersion = machoVersion
    self.bootVersion = bootVersion
    self.bootBuild = bootBuild
    self.bootCodename = bootCodename
    self.bootRegion = bootRegion
    self.userName = userName
    self.userPassword = userPassword
    self.userPasswordHash = userPasswordHash
    self.userLanguageID = userLanguageID
    self.userAffiliateID = userAffiliateID

    def getTuple(self):
        return (
            self.clientChallenge,
            {
                'macho_version': self.machoVersion,
                'boot_version': self.bootVersion,
                'boot_build': self.bootBuild,
                'boot_codename': self.bootCodename,
                'boot_region': self.bootRegion,
                'user_name': self.userName,
                'user_password': self.userPassword,
                'user_password_hash': self.userPasswordHash,
                'user_languageid': self.userLanguageID,
                'user_affiliateid': self.userAffiliateID
            })


class CryptoServerHandshake:

    def __init__(self, serverChallenge, funcMarshaledCode, verification, context,
        challengeResponseHash, machoVersion, bootVersion, bootBuild, bootCodename
        bootRegion, clusterUserCount, proxyNodeID, userLogonQueuePosition, imageServerURL):
    self.serverChallenge = serverChallenge
    self.funcMarshaledCode = funcMarshaledCode
    self.verification = verification
    self.context = context
    self.challengeResponseHash = challengeResponseHash
    self.machoVersion = machoVersion
    self.bootVersion = bootVersion
    self.bootBuild = bootBuild
    self.bootCodename = bootCodename
    self.bootRegion = bootRegion
    self.clusterUserCount = clusterUserCount
    self.proxyNodeID  = proxyNodeID
    self.userLogonQueuePosition = userLogonQueuePosition
    self.imageServerURL = imageServerURL

    def getTuple():
        return (
            self.serverChallenge,
            (
                self.funcMarshaledCode,
                self.verification
            ),
            self.context,
            {
                'challenge_responsehash': self.challengeResponseHash,
                'macho_version': self.machoVersion,
                'boot_version': self.bootVersion,
                'boot_build': self.bootBuild,
                'boot_codename': self.bootCodename,
                'boot_region': self.bootRegion,
                'cluster_usercount': self.clusterUserCount,
                'proxy_nodeid': self.proxyNodeID,
                'user_logonqueueposition': self.userLogonQueuePosition,
                'config_vals': {'imageServerURL': self.imageServerURL}
            })


class CryptoHandshakeResult:

    def __init__(self, challengeResponseHash, funcOutput, funcResult):
        self.challengeResponseHash = challengeResponseHash
        self.funcOutput = funcOutput
        self.funcResult = funcResult

    def getTuple(self):
        return (
            self.challengeResponseHash,
            self.funcOutput,
            self.funcResult
            )
            
class CryptoHandshakeResultAck:

    def __init__(self, liveUpdates, languageID, userID, maxSessionTime, userType,
        role, address, inDetention, clientHash, userClientID):
    self.liveUpdates = liveUpdates
    self.languageID = languageID
    self.userID = userID
    self.maxSessionTime = maxSessionTime
    self.userType = userType
    self.role = role
    self.address = address
    self.inDetention = inDetention
    self.clientHash = clientHash
    self.userClientID = userClientID

    def getTuple(self):
        return {
            {'liveUpdates': liveUpdates},
            {'session_init': {
                            'languageID': self.languageID,
                            'userid': self.userID,
                            'maxSessionTime': self.maxSessionTime, #seen None
                            'userType': self.userType,
                            'role': self.role,
                            'address': self.address,
                            'inDetention': self.inDetention
                            }
            },
            {'client_hash': self.clientHash},
            {'user_clientid': self.userClientID}
        }









