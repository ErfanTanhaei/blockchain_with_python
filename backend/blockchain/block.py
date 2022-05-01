import time
from backend.blockchain.crypto_hash import crypto_hash
from backend.config import mine_rate
from backend.blockchain.hex_to_binary import hex_to_binary

genesis_data ={
    "timestamp" : 1 ,
    "last_hash" : "last_genesis_hash" ,
    "hash" : "genesis_hash" ,
    "data" : [],
    "difficullty" : 4 ,
    "nonce" : "genesis_nonce"

}
class Block:
    """
    Blocks : for store data in there.
    each block store transaction in blockchain.
    """
    def __init__(self , timestamp , last_hash , hash , data , difficullty , nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficullty = difficullty
        self.nonce = nonce

    def __repr__(self):
        
        return (
            'Block('
            f'timestamp : {self.timestamp},'
            f'last_hash : {self.last_hash},'
            f'hash : {self.hash},'
            f'data : {self.data},'
            f'difficullty : {self.difficullty},'
            f'nonce : {self.nonce})'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        serialize the block into dictionary
        """
        return self.__dict__


    @staticmethod
    def mine_block(last_block, data):
        """
        mine a block baseed on the given last block and data until a block hash is found that meets the leading 0's
        proof of work requirement
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficullty = Block.adjust_difficullty(last_block , timestamp)
        nonce = 0
        hash = crypto_hash(timestamp , last_hash , data , difficullty , nonce)

        while hex_to_binary(hash)[0:difficullty] != '0' *difficullty :
            nonce += 1
            timestamp = time.time_ns()
            difficullty = Block.adjust_difficullty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficullty, nonce)

        return Block(timestamp, last_hash, hash, data , difficullty , nonce)


    @staticmethod
    def from_json(block):
        return Block(**block)


    @staticmethod
    def genesis():
        """
        generate the genesis block
        """
        return Block(**genesis_data)



    @staticmethod
    def adjust_difficullty(last_block , new_timestamp):
        """
        calculate new difficulty according to the mine_rate
        """
        if (new_timestamp - last_block.timestamp) < mine_rate:

            return  last_block.difficullty + 1


        if(last_block.difficullty -1 ) > 0:

            return last_block.difficullty -1


        return 1

    @staticmethod
    def is_valid_block(last_block , block):
        """
        validate block by last hash & hash & difficulty
        """
        if last_block.hash != block.last_hash :

            raise Exception("the block last_hash must be currect")


        if hex_to_binary(block.hash)[0:block.difficullty] != "0" * block.difficullty :

            raise Exception("the proof of requirment is not met")


        if abs(last_block.difficullty - block.difficullty) > 1 :

            raise Exception("the block difficulty is not currecet")


        reconstructed_hash = crypto_hash(
            block.timestamp,
            last_block.hash,
            block.difficullty,
            block.data,
            block.nonce
        )

        if reconstructed_hash != block.hash :

            raise Exception("the hash must be correct")



if __name__ == "__main__":
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block , 'bad block')
    bad_block.last_hash = "jfsal"
    try:
        Block.is_valid_block(genesis_block , bad_block)
    except Exception as e:
        print(e)
