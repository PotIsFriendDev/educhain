from typing import List
from .transaction import Transaction

class Mempool:
    """
    The Mempool (Memory Pool) is a temporary storage area for transactions
    that have been broadcast to the network but not yet included in a block.
    """
    def __init__(self):
        self._pending_transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        """Validates and adds a transaction to the pool."""
        # In a real system, we would verify the sender has enough balance here.
        self._pending_transactions.append(transaction)

    def get_all_transactions(self) -> List[Transaction]:
        """Returns all pending transactions to be included in the next block."""
        return self._pending_transactions

    def clear(self):
        """Empties the pool after transactions are mined into a block."""
        self._pending_transactions = []

    def __len__(self):
        return len(self._pending_transactions)
