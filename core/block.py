import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List
from .transaction import Transaction

@dataclass
class Block:
    """
    A Block is a container for a set of transactions.

    Each block contains a 'fingerprint' (hash) of itself and the hash
    of the previous block, creating a secure chain.
    """
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = None

    def __post_init__(self):
        if self.hash is None:
            self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Computes the SHA-256 hash of the block's contents.

        The hash depends on all attributes. If a single transaction
        is changed, the hash will change completely, breaking the chain.
        """
        # We use a sorted dictionary for transactions to ensure consistent hashing
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def update_hash(self):
        """Recomputes the hash after the nonce has been changed during mining."""
        self.hash = self.compute_hash()

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash[:10]}..., nonce={self.nonce})"
