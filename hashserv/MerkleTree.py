import hashlib


# Can define and pass other hash functions here if you don't want to use SHA256
def sha256(content):
    """Finds the sha256 hash of the content."""
    content = content.encode('utf-8')
    return hashlib.sha256(content).hexdigest()


class MerkleBranch:
    def __init__(self, left, right, hash_f=sha256):
        """Build a Merkle branch."""
        self.left = left
        self.right = right
        self.hash_f = hash_f

    def get_parent(self):
        """Get the parent of the branch."""
        return self.hash_f(self.left + self.right)


class MerkleProof:
    def __init__(self, target, hash_f=sha256):
        """Build a Merkle proof."""
        self.target = target
        self.hash_f = hash_f


class MerkleTree:
    def __init__(self, hash_f=sha256):
        """Simplistic Merkle tree. Defaults to sha256."""
        self.leaves = []
        self.hash_f = hash_f

    def add_content(self, content):
        """Hashes a content string and adds to the leaves."""
        self.leaves.append(self.hash_f(content))

    def add_hash(self, ahash):
        """Adds a single hash to the to the leaves."""
        self.leaves.append(ahash)

    def merkle_root(self):
        """Take a list of hashes, and return the root merkle hash."""
        # Generate list we can mutate
        hashes = self.leaves

        # Reduce list till we have a merkle root
        while len(hashes) > 1:
            hashes = self.merkle_pair(hashes)
        return hashes[0]

    def merkle_pair(self, hashes, target=None):
        """
        Take a list of hashes, and return the parent row in the tree
        of merkle hashes. Optionally takes a target, in which case it
        will return a branch of the proof.
        """
        # if odd then append first entry to the end of the list
        if len(hashes) % 2 == 1:
            hashes = list(hashes)
            hashes.append(hashes[-1])
        l = []
        for i in range(0, len(hashes), 2):
            l.append(self.hash_f(hashes[i] + hashes[i + 1]))
            if target == hashes[i] or target == hashes[i + 1]:
                return MerkleBranch(hashes[i], hashes[i + 1], self.hash_f)
        return l

    def merkle_proof(self, target):
        """Gives the merkle proof of a particular leaf in the root."""
        # Generate list we can mutate
        hashes = self.leaves
        proof = []

        # Reduce list till we have a merkle root, but extra target
        while len(hashes) > 1:
            branch = self.merkle_pair(hashes, target)
            proof.append(branch)
            target = branch.get_parent()
            hashes = self.merkle_pair(hashes)

        return proof