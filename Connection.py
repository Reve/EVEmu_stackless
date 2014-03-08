import logging
import stackless

import EVESession


class Connection:
    def __init__(self, clientsocket, address, control):
        # Create manager channel which can inform us
        # about the results of any external manager's
        # actions (logging in, registering, etc)
        manager = stackless.channel()

        # Handle Messages in one tasklet
        stackless.tasklet(self.network)(clientsocket, address)

        self.control = control
        self.manager = manager
        
        self.session = EVESession()
        self.step = 0
        
        stackless.schedule()

    def network(self, clientsocket, address):
        logging.info("Client %s:%s connected!" % (address[0], address[1]))

        data = ''
        while clientsocket.connect:
            
            if EVESession.EVE_VERSION_EXCHANGE == self.step:
                data = self.session.sendVersionExchange(0)
                clientsocket.sendall(data)
            elif EVESession.EVE_COMMAND == self.step:
                pass
            elif EVESession.EVE_CRYPTO == self.step:
                pass
            elif EVESession.EVE_AUTHENTICATION == self.step:
                pass
            elif EVESession.EVE_FUNC_RESULT == self.step:
                pass
            elif EVESession.EVE_PACKET_READING == self.step:
                pass

            data = clientsocket.recv(4096)
            if data == '':
                break
            
            logging.info(data)
            
            data = ''
            stackless.schedule()

        # Loop over, connection is broken
        self.close(clientsocket)

    def close(self, clientsocket):
        clientsocket.close()





