import sys
import Ice
import remotetypes
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from typing import List

class Cliente(Ice.Application):
    def run(self, argv: List[str]) -> int:
        proxy = self.communicator().stringToProxy(argv[1])
        print(proxy)
        factory_service = remotetypes.RemoteTypes.FactoryPrx.checkedCast(proxy)
        factory_service.get(rt.TypeName.RDict,None)
        return 0
    

if __name__ == '__main__':
    cliente = Cliente()
    sys.exit(cliente.main(sys.argv))
        