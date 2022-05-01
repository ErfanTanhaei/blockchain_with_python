hex_to_binary_table ={
    "0" : "0000",
    "1" : "0001",
    "2" : "0010",
    "3" : "0011",
    "4" : "0100",
    "5" : "0101",
    "6" : "0110",
    "7" : "0111",
    "8" : "1000",
    "9" : "1001",
    "a" : "1010",
    "b" : "1011",
    "c" : "1100",
    "d" : "1101",
    "e" : "1110",
    "f" : "1111",
}

def hex_to_binary(hex_num):
    binary = ""
    for char in hex_num :
        binary += hex_to_binary_table[char]
    return binary
  

if __name__ == "__main__":
    num = 451
    hex_num = hex(num)[2:]
    binary = hex_to_binary(hex_num)
    print(f"hex num : {hex_num}")
    print(f"binary num : {binary}")
    print(f"num : {int(binary , 2)}")