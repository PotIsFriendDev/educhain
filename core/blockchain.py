import time
from typing import List
from .block import Block
from .transaction import Transaction
from .mempool import Mempool

class Blockchain:
    """
    The Blockchain class manages the chain of blocks, enforces consensus
    rules, and handles the mining process.
    """
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.mempool = Mempool()
        self._create_genesis_block()

    def _create_genesis_block(self):
        """
        The Genesis Block is the first block in any blockchain.
        It's hardcoded because it has no previous block to reference.
        """
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0" * 64
        )
        self.chain.append(genesis_block)

    def proof_of_work(self, block: Block):
        """
        The Proof-of-Work (PoW) mechanism.

        The goal is to find a 'nonce' such that the block's hash starts with
        a specific number of zeros (defined by self.difficulty).

        Why do this? It makes mining 'expensive' in terms of CPU time,
        preventing attackers from easily rewriting the chain history.
        """
        target = "0" * self.difficulty

        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.update_hash()

        return block

    def mine(self) -> Block:
        """
        Mines a new block using all pending transactions in the mempool.
        """
        # 1. Prepare the block with current state
        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.mempool.get_all_transactions(),
            previous_hash=last_block.hash
        )

        # 2. Perform Proof-of-Work (This is where the "mining" happens)
        mined_block = self.proof_of_work(new_block)

        # 3. Add to chain and clear the mempool
        self.chain.append(mined_block)
        self.mempool.clear()

        return mined_block

    def is_chain_valid(self) -> bool:
        """
        Validates the entire blockchain.

        A chain is valid if:
        1. Every block's hash is correct based on its contents.
        2. Every block's previous_hash matches the actual hash of the previous block.
        3. Every block (except genesis) satisfies the Proof-of-Work difficulty.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Check if current block hash is correct
            if current.hash != current.compute_hash():
                return False

            # Check if it links correctly to the previous block
            if current.previous_hash != previous.hash:
                return False

            # Check if PoW was actually performed
            if current.hash[:self.difficulty] != "0" * self.difficulty:
                return False

        return True

    def get_status(self):
        """Returns basic status of the blockchain."""
        return {
            "height": len(self.chain),
            "difficulty": self.difficulty,
            "pending_transactions": len(self.mempool)
        }
