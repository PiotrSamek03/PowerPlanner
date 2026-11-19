class Agd:
    def __init__(self, name: str, power: float, fuse_name: str = None, color: str = None):
        self.name = name
        self.power = power
        self.fuse_name = fuse_name
        self.color = color

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "power": self.power,
            "fuse_name": self.fuse_name,
            "color": self.color
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Agd":
        return cls(
            name=data.get("name", ""),
            power=data.get("power", 0),
            fuse_name=data.get("fuse_name"),
            color=data.get("color")
        )