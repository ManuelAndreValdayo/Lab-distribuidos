import json
from typing import Optional
import Ice
import RemoteTypes as rt

class RemoteList(rt.RList):
    """Implementation of the remote interface RList with JSON persistence."""

    def __init__(self, identifier: str = None) -> None:
        """Initialise a RemoteList with an optional identifier for JSON persistence."""
        self.identifier = identifier or "default_list"
        self._storage_ = []
        self._load_from_json()

    def _get_json_file(self) -> str:
        """Get the filename for the JSON storage."""
        return f"{self.identifier}_rlist.json"

    def _save_to_json(self) -> None:
        """Save the current state of the list to a JSON file."""
        with open(self._get_json_file(), 'w') as file:
            json.dump(self._storage_, file)

    def _load_from_json(self) -> None:
        """Load the state of the list from a JSON file if it exists."""
        try:
            with open(self._get_json_file(), 'r') as file:
                self._storage_ = json.load(file)
        except FileNotFoundError:
            self._storage_ = []

    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Append an item to the list and save to JSON."""
        self._storage_.append(item)
        self._save_to_json()

    def pop(self, index: Optional[int] = None, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an item from a specific position in the list and save to JSON."""
        try:
            if index is None:
                value = self._storage_.pop()
            else:
                value = self._storage_.pop(index)
            self._save_to_json()
            return value
        except IndexError as error:
            raise rt.IndexError("Index out of range") from error

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """Retrieve the item at the given position in the list."""
        try:
            return self._storage_[index]
        except IndexError as error:
            raise rt.IndexError("Index out of range") from error

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the list and save to JSON."""
        try:
            self._storage_.remove(item)
            self._save_to_json()
        except ValueError as error:
            raise rt.KeyError(item) from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the list."""
        return len(self._storage_)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the list contains the given item."""
        return item in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal list."""
        contents = list(self._storage_)
        return hash(repr(contents))