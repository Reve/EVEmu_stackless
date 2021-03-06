# Packets for handling Crypto Handshake
class VersionExchangeServerPkt:
    def __init__(self, birthday, machoNet, userCount, versionNumber, buildVersion, projVersion):
        self.birthday = birthday
        self.machoNet = machoNet
        self.userCount = userCount
        self.versionNumber = versionNumber
        self.buildVersion = buildVersion
        self.projVersion = projVersion

    def encode(self):
        return (
            self.birthday,
            self.machoNet,
            self.userCount,
            self.versionNumber,
            self.buildVersion,
            self.projVersion,
            None  # update_info
        )


class VersionExchangeClientPkt:
    def __init__(self, pkt):
        print(pkt)
        self.birthday = pkt[0]
        self.machoNet = pkt[1]
        self.userCount = pkt[2]
        self.versionNumber = pkt[3]
        self.buildVersion = pkt[4]
        self.projVersion = pkt[5]

    def encode(self):
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

    def encode(self):
        return None, self.queuePosition


class NetCommand_VK:
    def __init__(self, vipKey):
        self.vipKey = vipKey

    def encode(self):
        return None, self.vipKey


class CryptoRequestPacket:
    def __init__(self, keyVersion, keyParams):
        self.keyVersion = keyVersion
        self.keyParams = keyParams

    def encode(self):
        return self.keyVersion, self.keyParams


class CryptoAPIRequestParams:
    def __init__(self, sessionKey, hashMethod, sessionKeyLength, provider, sessionKeyMethod):
        self.sessionKey = sessionKey
        self.hashMethod = hashMethod
        self.sessionKeyLength = sessionKeyLength
        self.provider = provider
        self.sessionKeyMethod = sessionKeyMethod

    def encode(self):
        return ({
                    'crypting_sessionkey': self.sessionKey,
                    'signing_hashmethod': self.hashMethod,
                    'crypting_sessionkeylength': self.sessionKeyLength,
                    'crypting_securityprovidertype': self.provider,
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

    def encode(self):
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
    serverChallenge = None
    funcMarshaledCode = None
    verification = None
    context = None
    challengeResponseHash = None
    machoVersion = None
    bootVersion = None
    bootBuild = None
    bootCodename = None
    bootRegion = None
    clusterUserCount = None
    proxyNodeID = None
    userLogonQueuePosition = None
    imageServerURL = None

    def __init__(self):
        pass

    def encode(self):
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
    challengeResponseHash = None
    funcOutput = None
    funcResult = None

    def __init__(self):
        pass

    def encode(self):
        return (
            self.challengeResponseHash,
            self.funcOutput,
            self.funcResult
        )


class CryptoHandshakeResultAck:
    liveUpdates = None
    languageID = None
    userID = None
    maxSessionTime = None
    userType = None
    role = None
    address = None
    inDetention = None
    clientHash = None
    userClientID = None
    
    def __init__(self):
        pass    

    def encode(self):
        return {
            'liveUpdates': self.liveUpdates,
            'session_init': {
                'languageID': self.languageID,
                'userid': self.userID,
                'maxSessionTime': self.maxSessionTime,  #seen None
                'userType': self.userType,
                'role': self.role,
                'address': self.address,
                'inDetention': self.inDetention
            },
            'client_hash': self.clientHash,
            'user_clientid': self.userClientID
        }









