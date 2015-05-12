def latest_block(conn):
    """Give us the lastest block number."""
    query = "SELECT Count(*) FROM block_table"
    cur = conn.execute(query)
    return int(cur.fetchone()[0])


def latest_hash(conn):
    """Give us the lastest hash from DB."""
    query = "SELECT * FROM hash_table ORDER BY id DESC"
    cur = conn.execute(query)
    return int(cur.fetchone()[0])