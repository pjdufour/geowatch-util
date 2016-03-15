class GeoWatchBuffer(object):

    # Public
    limit = None
    check_limit = False

    def add_message(self, message):
        pass

    def add_messages(self, messages):
        pass

    def get_messages(self):
        pass

    def pop_messages(self, count=-1):
        pass

    def full(self):
        if self.limit > 0:
            return self.size() >= self.limit
        else:
            return False

    def empty(self):
        return self.size() == 0

    def size(self):
        pass

    def clear(self):
        pass

    def __init__(self, limit=0, check_limit=False):
        self.limit = limit
        self.check_limit = check_limit

    def close(self):
        self.clear()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

class GeoWatchBufferLocalMemory(object):

    # Private
    _messages = []

    def add_message(self, message):
        if self.check_limit:
            if not self.full():
                self._messages.append(message)
            else:
                raise GeoWatchBufferError("The new message would have exceeded the buffer's limit of "+self.limit+".")
        else:
            self._messages.append(message)

    def add_messages(self, messages):
        if self.check_limit:
            if self.size() + len(messages) <= self.limit:
                self._messages.extend(messages)
            else:
                raise GeoWatchBufferError("The new messages would have exceeded the buffer's limit of "+self.limit+".")
        else:
            self._messages.extend(messages)

    def get_messages(self):
        return self._messages

    def pop_messages(self, count=-1):
        if count == -1 or count >= self.size():
            r = self._messages
            self.clear()
            return r
        else:
            r = self._messages[:count]
            self._messages = self._messages[count:]
            return r

    def size(self):
        return len(self._messages)

    def clear(self):
        self._messages = []

    def __init__(self,
        limit=0,
        check_limit=False):
        super(GeoWatchBufferLocalMemory, self).__init__(limit=limit, check_limit=check_limit)

class GeoWatchBufferMongoDB(object):

    # Public
    client = None
    db = None
    collection = None

    def add_message(self, message):
        if self.check_limit:
            if not self.full():
                self.collection.insert_one(messages)
            else:
                raise GeoWatchBufferError("The new message would have exceeded the buffer's limit of "+self.limit+".")
        else:
            self.collection.insert_one(message)

    def add_messages(self, messages):
        if self.check_limit:
            if self.size() + len(messages) <= self.limit:
                self.collection.insert_many(messages)
            else:
                raise GeoWatchBufferError("The new messages would have exceeded the buffer's limit of "+self.limit+".")
        else:
            self.collection.insert_many(messages)

    def get_messages(self):
        return [x for x in self.collection.find()]

    def pop_messages(self, count=-1):
        if count == -1 or count >= self.size():
            r = [x for x in self.collection.find()]
            self.clear()
            return r
        else:
            i = 0
            r = []
            for x in self.collection.find():
                if i >= count:
                    break
                r.append(x)
                i++
            self.collection.delete_many({})  # Need to adjust so it doesn't delete everything
            return r

    def size(self):
        return len(self.collection.find())

    def clear(self):
        self.collection.delete_many({})

    def __init__(self,
        limit=0,
        check_limit=False,
        db_host='localhost',
        db_port=27017,
        db_name=None,
        db_collection=None):
        super(GeoWatchBufferMongoDB, self).__init__(limit=limit, check_limit=check_limit)

        if db_host and db_port and db_name and db_collection:
            self.client = MongoClient(db_host, db_port)
            self.db = client[db_name]
            self.collection = db[db_collection]
        else:
            raise GeoWatchBufferError("MongoDB params missing.")


class GeoWatchBufferError(Exception):

    def __init__(self, * args, ** kwargs):
        super(GeoWatchBufferError, self).__init__(self, * args, ** kwargs)
