# HashMap class to create HashMap objects
class HashMap:
    # Entry class used to encapsulate pairs. Improves code readability.
    class Entry:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    # Initialize the hash map
    def __init__(self, initial_capacity=20):
        self.buckets = [[] for _ in range(initial_capacity)]

    # Insert function
    def add(self, key, value):
        bucket = hash(key) % len(self.buckets)
        bucket_items = self.buckets[bucket]

        for entry in bucket_items:
            if entry.key == key:
                entry.value = value
                return True

        entry = self.Entry(key, value)
        bucket_items.append(entry)
        return True

    # Search function
    def search(self, key):
        bucket = hash(key) % len(self.buckets)
        bucket_items = self.buckets[bucket]

        for entry in bucket_items:
            if entry.key == key:
                return entry.value

        return None

    # Remove function
    def hash_remove(self, key):
        bucket = hash(key) % len(self.buckets)
        bucket_items = self.buckets[bucket]

        for entry in bucket_items:
            if entry.key == key:
                bucket_items.remove(entry)
                return True

        return False