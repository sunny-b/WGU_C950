class HashTable(object):
    def __init__(self, size = 10):
        self._struct = self._create_struct(size)

    def insert(self, key, value):
        hashed_key = hash(key)
        bucket = self._find_bucket(hashed_key)

        extent = self._find_kv_pair(hashed_key, bucket)
        
        if len(extent) == 0:
            bucket.append([hashed_key, value])
        else:
            extent[1] = value

        return True

    def find(self, key):
        hashed_key = hash(key)
        bucket = self._find_bucket(hashed_key)

        kv_pair = self._find_kv_pair(hashed_key, bucket)
        
        if kv_pair:
            return kv_pair[1]

        raise Exception("key-value pair does not exist")
    
    def _create_struct(self, size):
        struct = []
        for i in range(size):
            struct.append([])

        return struct

    def _find_bucket(self, key):
        return self._struct[key % len(self._struct)]

    def _find_kv_pair(self, key, bucket):
        for kv_pair in bucket:
            if kv_pair[0] == key:
                return kv_pair

        return []


