import hashlib
import json

def crypto_hash(*args):
    """
    return a sha-256 hash of the given arguments
    """
    stringifid =sorted(map( lambda data : json.dumps(data), args))
    joined_data = ''.join(stringifid)
    return hashlib.sha256(joined_data.encode("utf-8")).hexdigest()



if __name__ == "__main__":

    # print(f'erfan , tanhaei , mohammad : {crypto_hash("erfan" , "tanhaei" , 2)}')
    data = json.dumps(1)
    print(hashlib.sha256(data.encode('utf-8')).hexdigest())