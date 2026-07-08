# 🎓 EduChain: Learn Blockchain by Building One

EduChain is a simplified, fully functional blockchain implementation in Python. It's designed specifically for educational purposes, stripping away the complexity of real-world networks (like P2P networking and complex cryptography) to focus on the core logic: **Hashing, Proof-of-Work, and Immutability**.

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the directory or create it
cd educhain
pip install -r requirements.txt
```

### 2. Running the Project
Start the API server using uvicorn:
```bash
# From the root directory of the project
uvicorn api.main:app --reload
```

### 3. Interacting with the Blockchain
Once the server is running, visit:
👉 **`http://127.0.0.1:8000/docs`**

This is the **Swagger UI**, a built-in interactive documentation page where you can test the blockchain without writing any code.

**Try this sequence:**
1. `GET /status` $\rightarrow$ See the genesis block (height 1).
2. `POST /transactions/new` $\rightarrow$ Add a few transactions (e.g., Alice $\to$ Bob: 10).
3. `GET /status` $\rightarrow$ Notice the `pending_transactions` count increased.
4. `GET /mine` $\rightarrow$ Trigger the mining process. This will take a few seconds as your CPU solves the PoW puzzle.
5. `GET /chain` $\rightarrow$ View the newly created block and its transactions.
6. `GET /validate` $\rightarrow$ Confirm the chain is still valid.

---

## 📚 Core Concepts Explained

### 1. The Block & Hashing
Every block has a unique `hash`. This hash is created by taking all the block's data (index, timestamp, transactions, previous hash, and nonce) and passing it through the **SHA-256** algorithm.
**Why?** If you change one character in a transaction, the hash changes completely. This makes the blockchain "tamper-evident".

### 2. The Chain (Immutability)
Each block stores the `previous_hash` of the block before it. This creates a link. 
If an attacker changes a block in the past:
1. That block's hash changes.
2. The *next* block's `previous_hash` no longer matches.
3. The entire chain from that point forward becomes invalid.

### 3. Proof-of-Work (PoW)
Mining isn't just about adding blocks; it's about solving a puzzle. In EduChain, the puzzle is: *"Find a number (nonce) that, when added to the block, makes the resulting hash start with X zeros."*
**Why?** This requires computational effort. It ensures that blocks aren't created too quickly and makes it prohibitively expensive for an attacker to rewrite history (they would have to re-mine every single block).

### 4. The Mempool
Transactions don't go straight into the blockchain. They wait in the **Mempool**. Miners pick transactions from the pool, package them into a block, and then mine that block.

---

## 🛠 Project Structure
- `core/transaction.py`: Defines the value transfer.
- `core/block.py`: Defines the block structure and hashing.
- `core/blockchain.py`: The logic for mining and validation.
- `core/mempool.py`: Temporary storage for pending transactions.
- `api/main.py`: The REST API layer using FastAPI.
