# hashserv

[![Build Status](https://travis-ci.org/Storj/hashserv.svg?branch=master)]
(https://travis-ci.org/Storj/hashserv) 
[![Coverage Status](https://coveralls.io/repos/Storj/hashserv/badge.svg?branch=master)](https://coveralls.io/r/Storj/hashserv?branch=master)

# What is this?

Basically we want to prove some data existed at a certain point and time, we call this
Proof of Existence. We can do that by finding the cryptographic hash of some data, then
inserting that hash into the Bitcoin blockchain. Since the Bitcoin blockchain is an immutable
and secure ledger, we can prove that the data existed at the time of insertion, like a
mathematical notary. Unfortunately that insertion costs money, around $0.02, so it
becomes expensive if I wanted to do this for 10,000+ documents. 

Instead we can take that data and put it in a 
[Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree), and insert the Merkle root into
the Bitcoin blockchain. In this case we only have to do one transaction, but still can do
Proof of Existence for any data item that is in our Merkle Tree.

**tldr;** A federated server for building blockchain notarized Merkle trees. 

# API
Add a hash to the queue for the next block. Returns the block number that the data will
be inserted into. In some cases the hash is a duplicate, so the API will return the block
number that the hash is in.
    
    GET /api/submit/<sha256_hash>
        Parameters:
        - sha256_hash
        Returns:
        - block_num
Sample Output:

    47

Returns the content of a particular block.
    
    GET /api/block/<block_num>
		Parameters:
		- block_num
		Returns:
		- Block data
		
Sample Output:

    {
      "block_num": 1,
      "closed": true,
      "leaves": [
        "da374a516e995319b65200dac1a1846bca567fa815ec069340d6a786145192c4",
        "00d8f97417e848cb7df29e0e9834e2a8cab9f411d7d2f95ee56ef5083010a84c"
      ],
      "merkle_root": "8087f1a140d5ebf7753812a2ac92f9335eddf6562509f63b672783e400a5ebb8",
      "tx_id": null
    }
    
The latest block on this federated server.
    
    GET /api/block/latest_block
        Returns:
        - Block number of the latest block
        
Sample Output:

    78

Return a Merkle proof for an inserted item with a closed block.

    GET /api/proof/<sha256_hash>
         Parameters:
        - sha256_hash
        Returns:
        - Merkle proof and other JSON data
        
Sample Output:

    {
      "merkle_root": "f8f8e3755e93a24284c97dc71d5daa3c25750458d4ebbd33f03ba507053c9748",
      "proof": [
        {
          "left": "e970c5e381cc24fbfa478f711a50ce8577d36ab8cdb21e10e663e68eb051ff5b",
          "parent": "075d3bed54db688da338a70e1c5c1a9437551571a3aeb79e8a11a1c1e9a1ab44",
          "right": "e970c5e381cc24fbfa478f711a50ce8577d36ab8cdb21e10e663e68eb051ff5b"
        },
        {
          "left": "77ef2b0d1fb3fab2c98bfbd64938b4c69430b2f11b452e825180771661bea76b",
          "parent": "f8f8e3755e93a24284c97dc71d5daa3c25750458d4ebbd33f03ba507053c9748",
          "right": "075d3bed54db688da338a70e1c5c1a9437551571a3aeb79e8a11a1c1e9a1ab44"
        }
      ],
      "target": "e970c5e381cc24fbfa478f711a50ce8577d36ab8cdb21e10e663e68eb051ff5b",
      "tx_id": null
    }