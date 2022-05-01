import random
import os

from flask import Flask , jsonify , request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool


block_chain = Blockchain()
transaction_pool = TransactionPool()
pubsub = PubSub(block_chain , transaction_pool)
wallet = Wallet(block_chain)
app = Flask(__name__)


@app.route('/')
def route_default():
    return 'Welcome to my Blockchain Project'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(block_chain.to_json())


@app.route('/blockchain/mine')
def route_mine():
    trx_data = transaction_pool.teransaction_data()
    trx_data.append(Transaction.reward_transaction(wallet).to_json())
    block_chain.add_block(trx_data)
    block = block_chain.chain[-1]
    pubsub.broadcast_block(block)

    transaction_pool.clear_blockchain_transaction(block_chain)

    return jsonify(block.to_json())


@app.route('/wallet/transact' , methods=['POST'])
def route_wallet_transact():
    trx_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)

    if transaction:
        transaction.update(wallet , trx_data['recepient'] , trx_data['amount'])

    else:
        transaction = Transaction(wallet , trx_data['recepient'] , trx_data['amount'])

    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address:':wallet.address , 'ballance:':wallet.ballance})


PORT = 5000

if os.environ.get("PEER") == "True":
    PORT = random.randint(5001,6000)

app.run(port=PORT)