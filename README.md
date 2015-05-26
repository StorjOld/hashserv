# hashserv

[![Build Status](https://travis-ci.org/Storj/hashserv.svg?branch=master)]
(https://travis-ci.org/Storj/hashserv) 
[![Coverage Status](https://coveralls.io/repos/Storj/hashserv/badge.svg?branch=master)](https://coveralls.io/r/Storj/hashserv?branch=master)

# What is this?

We want to prove some data existed at a certain point and time, we call this
Proof of Existence. We can do that by finding the cryptographic hash of some data, then
inserting that hash into the Bitcoin blockchain. Since the Bitcoin blockchain is an immutable
and secure public ledger, we can prove that the data existed at the time of insertion, like a
mathematical notary. Unfortunately that insertion costs money, around $0.03, so it
becomes expensive if I wanted to do this for 10,000+ documents. 

Instead we can take that data and put it in a 
[Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree), and insert the Merkle root into
the Bitcoin blockchain. For any of the items in the Merkle tree, as long as we have the Merkle proof,
we can prove that it is contained in that Merkle root notarized in the Bitcoin blockchain. 

Therefore we can notarize 10,000 documents for $0.03 instead of $300. It is 
recommended that the party notarizing their document or data hold on to the Merkle proof "receipt." 
This allows that party to prove that their document has been notarized in a specific Bitcoin transaction
in the absence of any other data.

**tldr;** A federated server for building blockchain notarized Merkle trees, and returning the Merkle
proof as a receipt. 

# Setup
In order to run you need to have a python config file in hashserv/config.py
By default hashserv/config.py is set to run on testnet with a test wallet.

    virtualenv -p /usr/bin/python3 venv # install virtualenv
    source venv/bin/activate # activate virtualenv
    python setup.py develop # install dependencies
    python -c 'from hashserv.app import init_db; init_db()' # init database
    python hashserv/app.py # start server

# API
Add a hash to the queue for the next block. Returns the block number that the data will
be inserted into. In some cases the hash is a duplicate, so the API will return the block
number that the hash is in.
    
    GET /api/submit/<sha256_hash>/
        Parameters:
        - sha256_hash
        Returns:
        - block_num
Sample Output:

    47

Returns the content of a particular block.
    
    GET /api/block/<block_num>/
		Parameters:
		- block_num
		Returns:
		- Block data
		
Sample Output:

    {
      "block_num": 1,
      "closed": true,
      "leaves": [
        "e1566f09e0deea437826514431be6e4bdb4fe10aa54d75aecf0b4cdc1bc4320c",
        "2f7f9092b2d6c5c17cfe2bcf33fc38a41f2e4d4485b198c2b1074bba067e7168",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      ],
      "merkle_root": "6a9a3c86d47f1fe12648c86368ecd9723ff12e3fc34f6ae219d4d9d3e0d60667",
      "tx_id": "012fdc0eb5ebae181e1197b4e9307731473118b0634d3ede749a562e9d11809e"
    }
    
The latest block on this federated server.
    
    GET /api/block/latest_block/
        Returns:
        - Block number of the latest block
        
Sample Output:

    78

Return a Merkle proof for an inserted item with a closed block.

    GET /api/proof/<sha256_hash>/
         Parameters:
        - sha256_hash
        Returns:
        - Merkle proof and other JSON data
        
Sample Output:

    {
      "merkle_root": "6a9a3c86d47f1fe12648c86368ecd9723ff12e3fc34f6ae219d4d9d3e0d60667",
      "proof": [
        {
          "left": "e1566f09e0deea437826514431be6e4bdb4fe10aa54d75aecf0b4cdc1bc4320c",
          "parent": "0fdd6b6895e15115c262f6acb9a6ae0c73248568b740454ab21591f8a533dd7f",
          "right": "2f7f9092b2d6c5c17cfe2bcf33fc38a41f2e4d4485b198c2b1074bba067e7168"
        },
        {
          "left": "0fdd6b6895e15115c262f6acb9a6ae0c73248568b740454ab21591f8a533dd7f",
          "parent": "6a9a3c86d47f1fe12648c86368ecd9723ff12e3fc34f6ae219d4d9d3e0d60667",
          "right": "3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33"
        }
      ],
      "target": "2f7f9092b2d6c5c17cfe2bcf33fc38a41f2e4d4485b198c2b1074bba067e7168",
      "tx_id": "012fdc0eb5ebae181e1197b4e9307731473118b0634d3ede749a562e9d11809e"
    }
    
Notarize the current block, and start a new one.

    GET /api/block/generate/
        Returns:
        - Number of block written in the blockchain
        
Sample Output:

    Block 3 Built.
