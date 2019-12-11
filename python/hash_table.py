class HashTable(object):
    def __init__(self, size = 10):
        self._struct = self._create_struct(size)

    # insert hashes the key and finds the modulo
    # it uses the modulo to find the appropriate bucket to append it to
    # Time complexity: O(n) - 'n' being the size of the bucket.
    def insert(self, key, value):
        hashed_key = hash(key)
        bucket = self._find_bucket(hashed_key)

        extent = self._find_kv_pair(hashed_key, bucket)
        
        if len(extent) == 0:
            bucket.append([hashed_key, value])
        else:
            extent[1] = value

        return True

    # find takes a key, hashes it and finds the matching bucket
    # It then loops through the bucket to find the appropriate value
    # Time complexity: O(n) - 'n' being the size of the bucket.
    def find(self, key):
        hashed_key = hash(key)
        bucket = self._find_bucket(hashed_key)

        kv_pair = self._find_kv_pair(hashed_key, bucket)
        
        if kv_pair:
            return kv_pair[1]

        raise Exception("key-value pair does not exist")
    
    # _create_struct loops through the hash table size and creates buckets that will be used later
    # Time complexity: O(n)
    def _create_struct(self, size):
        struct = []
        for i in range(size):
            struct.append([])

        return struct

    # _find_bucket uses the modulo of the hashed key to find the appropriate bucket
    # Time complexity: O(1)
    def _find_bucket(self, key):
        return self._struct[key % len(self._struct)]

    # _find_kv_pair loops through a bucket to find the appropriate key-value pair
    # Time complexity: O(n)
    def _find_kv_pair(self, key, bucket):
        for kv_pair in bucket:
            if kv_pair[0] == key:
                return kv_pair

        return []


