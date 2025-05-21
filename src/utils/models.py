from dataclasses import dataclass

from src.utils.constants import ID, PATTERN, MESSAGE, SEVERITY, INFO, REGEX, ADDITIONAL_PROPERTIES


@dataclass
class InlineRule:
    id: str
    pattern: str
    message: str
    severity: str = INFO
    regex: bool = False
    additional_properties: dict[str, str] = None

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "InlineRule":
        if ID not in data:
            raise ValueError(f"{ID} is required in {__class__.__name__}")
        if PATTERN not in data:
            raise ValueError(f"{PATTERN} is required in {__class__.__name__}")
        if MESSAGE not in data:
            raise ValueError(f"{MESSAGE} is required in {__class__.__name__}")

        return cls(
            id=data[ID],
            pattern=data[PATTERN],
            message=data[MESSAGE],
            severity=data.get(SEVERITY, INFO),
            regex=data.get(REGEX, False),
            additional_properties=data.get(ADDITIONAL_PROPERTIES, {})
        )
