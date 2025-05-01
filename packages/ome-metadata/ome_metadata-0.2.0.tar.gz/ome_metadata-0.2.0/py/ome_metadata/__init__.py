from __future__ import annotations

from . import ome_metadata_rs as rs  # noqa


class Ome(dict):
    @staticmethod
    def from_xml(xml: str) -> Ome:
        """Create the OME structure from an XML string"""
        new = Ome()
        new.update(rs.ome(str(xml)))
        return new

    def __dir__(self) -> list[str]:
        return list(self.keys()) + list(super().__dir__())

    def __getattr__(self, key: str) -> Ome | OmeList | int | float | str:
        try:
            new = self.__getitem__(key)
        except KeyError:
            raise AttributeError(f"'Ome' object has no attribute '{key}'")
        if isinstance(new, dict):
            return Ome(**new)
        elif isinstance(new, list):
            return OmeList(new)
        else:
            return new


class OmeList(list):
    def __getitem__(self, item: int) -> Ome | OmeList | int | float | str:
        new = super().__getitem__(item)
        if isinstance(new, dict):
            return Ome(**new)
        elif isinstance(new, list):
            return OmeList(new)
        else:
            return new
