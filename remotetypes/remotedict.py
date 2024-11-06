import json
from typing import Optional
import Ice
import RemoteTypes as rt

class RemoteDict(rt.RDict):
    """Implementation of the remote interface RDict with JSON persistence."""

    def __init__(self, identifier: str = None) -> None:
        """Initialise a RemoteDict with an optional identifier for JSON persistence."""
        self.identifier = identifier or "default_dict"
        self._storage_ = {}
        self._load_from_json()

    def _get_json_file(self) -> str:
        """Get the filename for the JSON storage."""
        return f"{self.identifier}_rdict.json"

    def _save_to_json(self) -> None:
        """Save the current state of the dictionary to a JSON file."""
        with open(self._get_json_file(), 'w') as file:
            json.dump(self._storage_, file)

    def _load_from_json(self) -> None:
        """Load the state of the dictionary from a JSON file if it exists."""
        try:
            with open(self._get_json_file(), 'r') as file:
                self._storage_ = json.load(file)
        except FileNotFoundError:
            self._storage_ = {}

    def setItem(self, key: str, item: str, current: Optional[Ice.Current] = None) -> None:
        """Set the value of a key in the dictionary and save to JSON."""
        self._storage_[key] = item
        self._save_to_json()

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Retrieve the value for the given key in the dictionary."""
        try:
            return self._storage_[key]
        except KeyError as error:
            raise rt.KeyError(key) from error

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Remove and return the value for the given key and save to JSON."""
        try:
            value = self._storage_.pop(key)
            self._save_to_json()
            return value
        except KeyError as error:
            raise rt.KeyError(key) from error

    def remove(self, key: str, current: Optional[Ice.Current] = None) -> None:
        """Remove a key from the dictionary and save to JSON."""
        try:
            del self._storage_[key]
            self._save_to_json()
        except KeyError as error:
            raise rt.KeyError(key) from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the dictionary."""
        return len(self._storage_)

    def contains(self, key: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the dictionary contains the given key."""
        return key in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal dictionary."""
        contents = list(self._storage_.items())
        contents.sort()
        return hash(repr(contents))