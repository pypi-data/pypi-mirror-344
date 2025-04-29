class CommandBuilder:
    def __init__(self):
        self._parts = []

    def add(self, part: str):
        """Adds a part to the CommandBuilder."""
        self._parts.append(part)
        return self

    def to_string(self) -> str:
        return " \\\n".join(self._parts)