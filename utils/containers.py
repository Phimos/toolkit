from typing import Any, Optional


class SlashDict(dict):
    def __init__(self, __map: dict = {}, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            __map[k] = v
        __map = {
            k: SlashDict(v) if isinstance(v, dict)
            else v for k, v in __map.items()
        }
        super().__init__(__map)

    def __getitem__(self, key: str, parent: Optional[str] = None):
        if "/" in key:
            cur, rest = key.split("/", maxsplit=1)
            if not super().__contains__(cur):
                if parent is None:
                    raise KeyError(key)
                else:
                    raise KeyError(
                        f"Dict under key {parent.__repr__()} does not have {cur.__repr__()}")
            parent = cur if parent is None else parent + '/' + cur
            return super().__getitem__(cur).__getitem__(rest, parent)
        else:
            if not super().__contains__(key):
                if parent is None:
                    raise KeyError(key)
                else:
                    raise KeyError(
                        f"Dict under key {parent.__repr__()} does not have {key.__repr__()} ")
            return super().__getitem__(key)

    def __repr__(self, out: bool = True) -> str:
        items = []
        for k, v in self.items():
            if isinstance(v, SlashDict):
                items.append(k.__repr__() + ": " + v.__repr__(False))
            else:
                items.append(k.__repr__() + ": " + v.__repr__())
        if out:
            return "SlashDict({" + ", ".join(items) + "})"
        else:
            return "{" + ", ".join(items) + "}"

    def __setitem__(self, key: str, value: Any) -> None:
        if "/" in key:
            cur, rest = key.split("/", maxsplit=1)
            if not super().__contains__(cur) or \
                    not isinstance(super().__getitem__(cur), SlashDict):
                super().__setitem__(cur, SlashDict())
            super().__getitem__(cur).__setitem__(rest, value)
        else:
            return super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        if "/" in key:
            cur, rest = key.split("/", maxsplit=1)
            return super().__getitem__(cur).__delitem__(rest)
        else:
            return super().__delitem__(key)

    def __contains__(self, key: str) -> bool:
        if "/" in key:
            cur, rest = key.split("/", maxsplit=1)
            if super().__contains__(cur):
                return super().__getitem__(cur).__contains__(rest)
            else:
                return False
        else:
            return super().__contains__(key)

    def keys(self, greedy: bool = False):
        if greedy:
            result = []
            for k, v in self.items():
                if isinstance(v, SlashDict):
                    for inner_key in v.keys(greedy=True):
                        result.append(k + "/" + inner_key)
                else:
                    result.append(k)
            return result
        else:
            return super().keys()

    def items(self, greedy: bool = False):
        if greedy:
            return [(k, self.__getitem__(k)) for k in self.keys(greedy=True)]
        else:
            return super().items()
