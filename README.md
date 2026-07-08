# 🎓 EduChain：通过构建区块链来学习区块链

EduChain 是一个用 Python 实现的简化且功能完整的区块链实现。它专为教学目的而设计，剔除了现实世界网络中的复杂性（如 P2P 网络和复杂的加密算法），旨在让学习者专注于核心逻辑：**哈希 (Hashing)、工作量证明 (Proof-of-Work) 和不可篡改性 (Immutability)**。

## 🚀 快速上手

### 1. 安装
```bash
# 克隆目录或创建它
cd educhain
pip install -r requirements.txt
```

### 2. 运行项目
使用 uvicorn 启动 API 服务器：
```bash
# 在项目的根目录下运行
uvicorn api.main:app --reload
```

### 3. 与区块链交互
服务器运行后，请访问：
👉 **`http://127.0.0.1:8000/docs`**

这是 **Swagger UI**，一个内置的交互式文档页面，您无需编写任何代码即可测试区块链。

**建议尝试以下操作顺序：**
1. `GET /status` $\rightarrow$ 查看创世区块（高度为 1）。
2. `POST /transactions/new` $\rightarrow$ 添加几笔交易（例如：Alice $\to$ Bob: 10）。
3. `GET /status` $\rightarrow$ 注意 `pending_transactions`（待处理交易）的数量增加了。
4. `GET /mine` $\rightarrow$ 触发挖矿进程。这需要几秒钟时间，因为您的 CPU 正在求解 PoW 谜题。
5. `GET /chain` $\rightarrow$ 查看新创建的区块及其包含的交易。
6. `GET /validate` $\rightarrow$ 确认链条是否依然有效。

---

## 📚 核心概念详解

### 1. 区块与哈希 (The Block & Hashing)
每个区块都有一个唯一的 `hash`。这个哈希值是通过将区块的所有数据（索引、时间戳、交易、前一区块哈希以及随机数 nonce）传递给 **SHA-256** 算法生成的。
**为什么？** 如果你修改交易中的一个字符，哈希值就会完全改变。这使得区块链具有“篡改可见”的特性。

### 2. 链条（不可篡改性 / Immutability）
每个区块都存储前一个区块的 `previous_hash`。这形成了一个链接。
如果攻击者修改了过去某个区块的内容：
1. 该区块的哈希值会改变。
2. *下一个* 区块的 `previous_hash` 将不再匹配。
3. 从该点起，整个链条都将失效。

### 3. 工作量证明 (Proof-of-Work, PoW)
挖矿不仅仅是添加区块，更是求解一个谜题。在 EduChain 中，谜题是：*“寻找一个数字 (nonce)，将其添加到区块中后，使生成的哈希值以 X 个零开头。”*
**为什么？** 这需要消耗计算资源。它确保了区块不会创建得太快，并且让攻击者重写历史的成本变得极高（他们必须重新挖掘每一个区块）。

### 4. 内存池 (The Mempool)
交易不会直接进入区块链，而是先在 **Mempool** 中等待。矿工从池中挑选交易，将它们打包进区块，然后对该区块进行挖矿。

---

## 🛠 项目结构
- `core/transaction.py`: 定义价值转移逻辑。
- `core/block.py`: 定义区块结构和哈希计算。
- `core/blockchain.py`: 实现挖矿和校验逻辑。
- `core/mempool.py`: 待处理交易的临时存储。
- `api/main.py`: 基于 FastAPI 的 REST API 层。
