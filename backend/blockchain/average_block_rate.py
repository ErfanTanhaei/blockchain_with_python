from backend.blockchain.blockchain import Blockchain
import time
from backend.config import second

block_chain = Blockchain()

times = []
for i in range(100):
    start_time = time.time_ns()
    block_chain.add_block(i)
    end_time = time.time_ns()
    time_to_mine = (end_time - start_time) / second
    times.append(time_to_mine)
    average_time = sum(times) / len(times)
    print(f"new block difficullty : {block_chain.chain[-1].difficullty}")
    print(f"time to mine block : {time_to_mine}s")
    print(f"avrage time : {average_time}s \n")



