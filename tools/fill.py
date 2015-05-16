import time
import random
import urllib.request
from hashserv.MerkleTree import sha256

url = "http://localhost:5000/api/submit/{0}"
delay = 0.5
loop = True

try:
    print("Will insert data until you CTRL+C...")
    while loop:
        ahash = sha256(str(random.random()))
        time.sleep(delay)
        urllib.request.urlopen(url.format(ahash))
        print(ahash)

except KeyboardInterrupt:
    loop = False
    print("Have a nice day!")
