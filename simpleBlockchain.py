import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data, nonce):
    value = str(index) + previous_hash + str(timestamp) + data + str(nonce)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", 0, calculate_hash(0, "0", time.time(), "Genesis Block", 0))

def create_new_block(previous_block, data, difficulty):
    index = previous_block.index + 1
    timestamp = time.time()
    previous_hash = previous_block.hash
    nonce = 0
    hash = calculate_hash(index, previous_hash, timestamp, data, nonce)
    while not hash.startswith('0' * difficulty):
        nonce += 1
        hash = calculate_hash(index, previous_hash, timestamp, data, nonce)
    return Block(index, previous_hash, timestamp, data, nonce, hash)

def is_chain_valid(blockchain, difficulty):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.hash != calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data, current_block.nonce):
            return False

        if current_block.previous_hash != previous_block.hash:
            return False

        if not current_block.hash.startswith('0' * difficulty):
            return False

    return True

# Creating the blockchain and adding the genesis block
difficulty = 4  # Number of leading zeroes required in the hash
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Adding new blocks to the blockchain
num_of_blocks_to_add = 5

for i in range(num_of_blocks_to_add):
    new_block_data = f"Block {i + 1} Data"
    new_block = create_new_block(previous_block, new_block_data, difficulty)
    blockchain.append(new_block)
    previous_block = new_block
    print(f"Block {new_block.index} has been added to the blockchain!")
    print(f"Hash: {new_block.hash}\n")

# Verifying the blockchain's integrity
print(f"Is blockchain valid? {is_chain_valid(blockchain, difficulty)}")
