class User:
    def __init__(self, name: str, ip: str):
        self.name = name
        self.props = {}
        self._devices = []
        self._ip = ip

    def __add__(self, prop: dict) -> None:
        self.props.extend(prop)

    def __sub__(self, prop: str) -> None:
        del self.props[prop]

    def __rshift__(self, obj: "instance") -> None:
        obj.props.extend(self.props)

    def __lshift__(self, obj: "instance") -> None:
        self.props.extend(obj.props)

    def computeDevices(self):
        return self._devices
