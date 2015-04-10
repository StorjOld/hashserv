import hashlib

def sha256(content):
	content = content.encode('utf-8')
	return hashlib.sha256(content).hexdigest()

def merkle_root(hashes, hash_f=sha256, target = None):
    """Take a list of hashes, and return the root merkle hash."""
    
    while len(hashes) > 1:
        hashes2 = hashes
        hashes = merkle_pair(hashes, hash_f)
        if not target == None:
        	proof = merkle_proof(hashes2, target, hash_f)
        	print(proofr)
    return hashes[0]

def merkle_pair(hashes, hash_f):
    """
    Take a list of hashes, and return the parent row in the tree
    of merkle hashes.
    """
    # if odd then append first entry to the end of the list
    if len(hashes) % 2 == 1:
        hashes = list(hashes)
        hashes.append(hashes[-1])
    l = []
    for i in range(0, len(hashes), 2):
        l.append(hash_f(hashes[i] + hashes[i+1]))
    return l

def merkle_proof(hashes, target, hash_f):
	# if odd then append first entry to the end of the list
    if len(hashes) % 2 == 1:
        hashes = list(hashes)
        hashes.append(hashes[-1])
    l = []
    for i in range(0, len(hashes), 2):
        if hashes[i] == target or hashes[i+1] == target:
        	result = hash_f(hashes[i] + hashes[i+1])
        	return(result, hashes[i], hashes[i+1])

if __name__ == "__main__":
	# Test 1
	hash_list1 = []
	hash_list1.append(sha256("test"))
	hash_list1.append(sha256("test2"))
	cor = merkle_root(hash_list1, sha256)
	res = '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f'
	assert(cor == res)

	# Test 2
	hash_list2 = []
	hash_list2.append(sha256("test"))
	hash_list2.append(sha256("test2"))
	target = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
	cor = merkle_root(hash_list2, sha256, target)

	# Test 3
	#hash_list1.append("test3")
	#cor = merkle_root(hash_list1, sha256)
	#res = 'e97635f0da94d8a1359f055eb3ddc8e37ed650e8d9dad18194945430a5e618fa'
	#assert(cor == res)