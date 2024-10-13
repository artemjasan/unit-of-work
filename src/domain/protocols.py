from typing import Protocol


class DomainEntity(Protocol):
    def __hash__(self) -> int:
        pass
