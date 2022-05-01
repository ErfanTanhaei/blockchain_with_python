import json
import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature , encode_dss_signature
from backend.config import ballance
from cryptography.hazmat.primitives import hashes , serialization
from cryptography.exceptions import InvalidSignature
from backend import config

class Wallet:
    
    def __init__(self , blockchain=None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(ec.SECP256K1() , default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()


    @property
    def ballance(self):
        return Wallet.calculate_ballance(self.blockchain , self.address)

    def sign(self , data):
        """
        generate a signature based on data with private key
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8') , 
            ec.ECDSA(hashes.SHA256())
            )) 


    def serialize_public_key(self):

        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')


    @staticmethod
    def verify(signutare , public_key , data):
        """
        verify a signature by using public key an data
        """
        (r , s) = signutare
        deserialize_public_key = serialization.load_pem_public_key(public_key.encode('utf-8') , default_backend())
        try:
            deserialize_public_key.verify(
                encode_dss_signature(r,s) , 
                json.dumps(data).encode('utf-8') , 
                ec.ECDSA(hashes.SHA256())
                )
            return True

        except InvalidSignature:
            return False

    @staticmethod
    def calculate_ballance(blockchain , address):
        """
        the ballance is found by adding the output value that belong to the address.
        """

        ballance = config.ballance

        if not blockchain:
            return ballance

        for block in blockchain.chain:
            for transaction in block.data:
                
                if transaction['input']['address'] == address:
                    ballance = transaction['output'][address]

                elif address in transaction['output']:
                    ballance += transaction['output'][address]
            
        return ballance




if __name__ == "__main__":

    wallet = Wallet()
    print(f'wallet: {wallet.__dict__}')
    data = {'erfan':'tanhaei'}
    sign = wallet.sign(data)
    print(f'signature : {sign}')
    verify = Wallet.verify(sign , wallet.public_key , data)
    print(verify)
    not_verify = Wallet.verify(sign , Wallet().public_key , data)
    print(not_verify)