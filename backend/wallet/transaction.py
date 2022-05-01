
import time
import uuid
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD , MINING_REWARD_INPUT

class Transaction():

    def __init__(self , sender_wallet=None , recepient=None , amount=None , id=None , input=None , output=None):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(sender_wallet , recepient , amount)
        self.input = input or self.create_input(sender_wallet , self.output)

    def create_output(self , sender_wallet , recepient , amount):
        
        if amount > sender_wallet.ballance:
            raise Exception('amount exeed balance')

        output = {}
        output[recepient] = amount
        output[sender_wallet.address] = sender_wallet.ballance - amount

        return output

    def create_input(self , sender_wallet , output):
        return{
            'timestamp' : time.time_ns() ,
            'amount' : sender_wallet.ballance ,
            'address' : sender_wallet.address , 
            'public_key': sender_wallet.public_key ,
            'signature': sender_wallet.sign(output),

        }

    def update(self , sender_wallet , recepient , amount):
        if amount > self.output[sender_wallet.address] :
            raise Exception('amount exceeds ballance')

        if recepient in self.output.values():
            self.output[recepient] = self.output[recepient] + amount

        else:
            self.output[recepient] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet , self.output)


    def to_json(self):

        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
      
        return Transaction(**transaction_json)

    @staticmethod
    def is_valid_transaction(trx):

        if trx.input == MINING_REWARD_INPUT:
            if list(trx.output.values()) != MINING_REWARD:
                raise Exception('invalid mining block')
            return
            
        output_total = sum(trx.output.values())

        if output_total != trx.input['amount']:
            raise Exception('invalid transaction output values')

        if not Wallet.verify(trx.input['signature'] , trx.input['public_key'] , trx.output):
            raise Exception('invalid signature')

    @staticmethod
    def reward_transaction(miner_wallet):

        output = {}
        output[miner_wallet.address] = MINING_REWARD

        return Transaction(input=MINING_REWARD_INPUT , output=output)

if __name__ == '__main__':
    trx = Transaction(Wallet() , 'recepient' , 10)
    print(trx.__dict__)