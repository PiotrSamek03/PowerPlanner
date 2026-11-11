class Fuse:
    def __init__(self, name, amps):
        self.name = name
        self.amps = amps
        self.state = "aktywny"
        self.attached_elements = []

    def attach_element(self, element):
        self.attached_elements.append(element)