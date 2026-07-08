from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.blockchain import Blockchain
from core.transaction import Transaction

app = FastAPI(title="EduChain API", description="An educational blockchain implementation")

# Initialize the blockchain global instance
# Difficulty 4 is a good balance for educational purposes (mine time ~1-5s)
blockchain = Blockchain(difficulty=4)

class TransactionModel(BaseModel):
    sender: str
    recipient: str
    amount: float

@app.get("/chain")
def get_chain():
    """Returns the full blockchain."""
    chain_data = []
    for block in blockchain.chain:
        block_dict = {
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": [tx.to_dict() for tx in block.transactions],
            "previous_hash": block.previous_hash,
            "nonce": block.nonce,
            "hash": block.hash
        }
        chain_data.append(block_dict)
    return {"length": len(chain_data), "chain": chain_data}

@app.post("/transactions/new")
def new_transaction(tx_model: TransactionModel):
    """Adds a new transaction to the mempool."""
    tx = Transaction(
        sender=tx_model.sender,
        recipient=tx_model.recipient,
        amount=tx_model.amount
    )
    blockchain.mempool.add_transaction(tx)
    return {"message": "Transaction added to mempool!", "transaction": tx.to_dict()}

@app.get("/mine")
def mine():
    """Triggers the mining of a new block."""
    # Check if there are transactions to mine (educational choice: allow empty blocks too)
    block = blockchain.mine()
    return {
        "message": "New block mined!",
        "block": {
            "index": block.index,
            "nonce": block.nonce,
            "hash": block.hash,
            "transactions": [tx.to_dict() for tx in block.transactions]
        }
    }

@app.get("/status")
def get_status():
    """Returns the current status of the blockchain."""
    return blockchain.get_status()

@app.get("/validate")
def validate():
    """Checks if the blockchain is currently valid."""
    is_valid = blockchain.is_chain_valid()
    return {"is_valid": is_valid, "message": "Blockchain is valid!" if is_valid else "Blockchain integrity compromised!"}
