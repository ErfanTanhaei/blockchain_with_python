
from backend.blockchain.block import Block
from backend.config import MINING_REWARD_INPUT
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

class Blockchain:
    """
    public ledger of transactions.
    data set of transactions.
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def __repr__(self):
        return f"this is blockchain one : {self.chain}"

    def add_block(self , data):
        self.chain.append(Block.mine_block(self.chain[-1] , data))

        
    def replace_chain(self , chain):
        """
        replace the local chain with incoming chain
        """
        if len(chain) <= len(self.chain):
            raise Exception("can not replace.the incoming chain must be longer")
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"the incoming chain is invalid {e}")
        self.chain = chain

    def to_json(self):
        """
        serialize blockchain into list of block
        """
        return list(map( lambda block : block.to_json(), self.chain))

    @staticmethod
    def is_valid_chain(chain):
        """
        validate the incoming chain
        -the chain must be start with genesis block
        -block must be formated correctly
        """
        if chain[0] != Block.genesis() :
            raise Exception("first chain must be genesis")

        for i in range(1 , len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block , block)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        -each transaction must only apear once in the chain
        -each block have only one reward transaction 
        -each transaction must be valid
        """
        transaction_ids = set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_block = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'transaction {transaction.id} not uniqe.')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_block:
                        raise Exception(
                            'there are can only one mining block.' \
                            f'check block with hash:{block.hash}'
                        )
                    has_mining_block = True

                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_ballance = Wallet.calculate_ballance(historic_blockchain , transaction.input['address'])
                    
                    if historic_ballance != transaction.input['amount']:
                        raise Exception(f'tranasction {transaction.id} has invalid input amount')

                Transaction.is_valid_transaction(transaction)




if __name__ == "__main__":

    blockchain_1 = Blockchain()
    blockchain_1.add_block("this is block one")
    blockchain_1.add_block("this is block two")
    print(blockchain_1)