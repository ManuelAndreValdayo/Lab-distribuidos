"""Needed classes to implement the Factory interface."""

import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error


class Factory(rt.Factory):
    """Skeleton for the Factory implementation."""
    def get(self,typeName,identifier=None):
        print(typeName)
        if typeName == rt.TypeName.RDict:
            return rt.RDict(identifier)
        else:
            # Handle unexpected typeName with an exception
            raise ValueError(f"Unknown TypeName: {typeName}")