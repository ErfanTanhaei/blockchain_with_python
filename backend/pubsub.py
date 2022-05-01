from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-f40f7892-7f6f-11ec-8ecc-dee9ee9643e0'
pnconfig.publish_key = 'pub-c-c28868d6-8dc8-42ca-b1a5-076b8f3fa251'
pnconfig.uuid = 'erfan'

CHANELLS = {
    'TEST':'TEST',
    'BLOCK':'BLOCK',
    'TRANSACTION':'TRANSACTION',
}

class PubSub():
    """
    handle the node in the network
    """
    def __init__(self , blockchain , transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANELLS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain , transaction_pool))

    def publish(self , channel , message):
        """
        pulish message to the channel
        """

        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self , block):
        """
        brodcast a block to all nodes
        """
        self.publish(CHANELLS['BLOCK'] , block.to_json())

    def broadcast_transaction(self , transaction):
        """
        brodcast a transaction to all nodes
        """

        self.publish(CHANELLS['TRANSACTION'] , transaction.to_json())



class Listener(SubscribeCallback):
    
    def __init__(self , blockchain , transaction_pool):

        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self , pubnub , message):
        print(f'\n Incoming message object:{message.message}')

        if message.channel == CHANELLS['BLOCK']:
            block = Block.from_json(message.message)
            new_blockchain = self.blockchain.chain[:]
            new_blockchain.append(block)

            try:
                self.blockchain.replace_chain(new_blockchain)
                self.transaction_pool.clear_blockchain_transaction(self.blockchain)
                print(f'replace chain successful')
            except Exception as e:
                print(f'did not replace chain:{e}')

        elif message.channel == CHANELLS['TRANSACTION']:
            transaction = Transaction.from_json(message.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n new transaction in transaction pool .')



if __name__ == '__main__':
    time.sleep(1)
    pubsub = PubSub()
    pubsub.publish( CHANELLS['TEST'], {'erfan':"tanhaei"})