class Fuse:
    def __init__(self, name: str, amps: float, state: str = "aktywny", attached_elements: list = None):
        self.name = name
        self.amps = amps
        self.state = state
        self.attached_elements = attached_elements if attached_elements is not None else []

    def attach_element(self, element):
        self.attached_elements.append(element)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "amps": self.amps,
            "state": self.state,
            "attached_elements": self.attached_elements
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Fuse":
        return cls(
            name=data.get("name", "Brak nazwy"),
            amps=data.get("amps", data.get("current_amp", 16)),
            state=data.get("state", "aktywny"),
            attached_elements=data.get("attached_elements", [])
        )