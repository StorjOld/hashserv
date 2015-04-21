# hashserv

[![Build Status](https://travis-ci.org/Storj/hashserv.svg?branch=master)](https://travis-ci.org/Storj/hashserv)

# What is this?

Basically we want to prove some data existed at a certain point and time, we call this Proof of Existence. We can do that by finding the cryptographic hash of some data, then inserting that hash into the Bitcoin blockchain. Since the Bitcoin blockchain is an immutable and secure ledger, we can prove that the data existed at the time of insertion, like a mathematical notary. Unfortunately that insertion costs money, around $0.02, so it becomes expensive if I wanted to do this for 10,000+ documents. 

Instead we can take that data and put it in a [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree), and insert the Merkle root into the Bitcoin blockchain. In this case we only have to do one transaction, but still can do Proof of Existence for any data item that is in our Merkle Tree.

**tldr;** A federated server for building blockchain notarized Merkle trees. 

# API
Add a hash to the queue for the next block. Returns the block number that the data will be inserted into.

	GET /api/submit/<sha256_hash>
        Parameters:
        - sha256_hash
        Returns:
        - block_num

Returns the content of a particular block.

	GET /api/block/<block_num>
		Parameters:
		- block_num
		Returns:
		- Block data