from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Transaction:
    """
    Represents a transfer of value between two parties.

    In a real blockchain, this would include digital signatures to
    prove the sender authorized the transaction. For this educational
    project, we use a simple sender/recipient model.
    """
    sender: str
    recipient: str
    amount: float
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().timestamp()

    def to_dict(self):
        """Converts the transaction to a dictionary for hashing and JSON serialization."""
        return asdict(self)

    def __repr__(self):
        return f"Transaction({self.sender} -> {self.recipient}: {self.amount})"
