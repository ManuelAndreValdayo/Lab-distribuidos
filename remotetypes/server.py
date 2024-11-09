"""remotetypes server application."""

import logging
import sys

import Ice

from remotetypes.factory import Factory


class Server(Ice.Application):
    """Ice.Application for the server."""

    def __init__(self) -> None:
        """Initialise the Server objects."""
        super().__init__()
        self.logger = logging.getLogger(__file__)

    def run(self, args: list[str]) -> int:
        """Execute the main server actions..

        It will initialise the needed middleware elements in order to execute the server.
        """
        factory_servant = Factory()
        adapter = self.communicator().createObjectAdapter("remotetypes")
        proxy = adapter.add(factory_servant, self.communicator().stringToIdentity("factory"))
        with open("proxy.txt","w") as archivo:
            archivo.write(proxy)
            
        self.logger.info('Proxyyy: "%s"', proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0

def main():
    """Handle the icedrive-authentication program."""
    app = Server()
    return app.main(sys.argv)

if __name__ == "__main__":
    main()