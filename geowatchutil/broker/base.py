import time


class GeoWatchBroker(object):

    verbose = False

    threads = None
    sleep_period = None
    deduplicate = False
    count = 1
    timeout = 5

    # Filters
    filter_last_one = False  # Filter messages to only last/latest message

    # Streaming Data
    consumers = None
    producers = None

    # Batch Storage
    stores_in = None
    stores_out = None

    def receive_message(self, message=None, filter_messages=True):
        self.receive_messages(messages=[message], filter_messages=filter_messages)

    def receive_messages(self, messages=None, filter_messages=True):
        if filter_messages:
            messages = self._cycle_filter(messages)
        self._cycle_out(messages=messages)
        self._post(messages=messages)

    def _pre(self):
        pass

    def _post(self, messages=None):
        pass

    def run(self, max_cycle=0):
        cycle = 1
        while True:
            if self.verbose:
                print "Cycle: ", cycle

            self._pre()

            messages = self._cycle_in()

            messages = self._cycle_filter(messages)

            self._cycle_out(messages=messages)

            self._post(messages=messages)

            if max_cycle > 0 and cycle == max_cycle:
                break

            cycle += 1
            time.sleep(self.sleep_period)

    def _cycle_in(self):
        messages_all = []
        messages_out = []

        if self.stores_in:
            for store in self.stores_in:
                messages = store.read()
                if messages:
                    messages_all.extend(messages)

        if self.consumers:
            if self.verbose:
                print "Receiving messages from "+str(len(self.consumers))+" consumers."
            for consumer in self.consumers:
                left = self.count - len(messages_all)
                if left > 0:
                    messages = consumer.get_messages(left, timeout=self.timeout)
                    # Returns messages encoded, such as list of strings, dicts/json, etc.
                    if messages:
                        messages_all.extend(messages)

        if self.verbose:
            print "Processing "+str(len(messages_all))+" messages."

        if self.deduplicate:
            seen = set()
            for message in messages_all:
                if message not in seen:
                    seen.add(message)
                    messages_out.append(message)
            if self.verbose:
                print str(len(messages_out))+" unique messages out of "+str(len(messages_all))+" messages."
        else:
            messages_out = messages_all

        return messages_out

    def _cycle_filter(self, messages=None):
        if self.filter_last_one:
            messages = [messages[-1]]

        return messages

    def _cycle_out(self, messages=None):
        if messages:
            if self.producers:
                for producer in self.producers:
                    producer.send_messages(messages)
            if self.stores_out:
                for store in self.stores_out:
                    store.write_messages(messages, flush=True)


    def close(self):
        for producer in self.producers:
            producer.close()
        for store in self.stores_out:
            store.close()

    def __init__(self, consumers=None, producers=None, stores_in=None, stores_out=None, count=1, timeout=5, threads=1, sleep_period=5, deduplicate=False, filter_last_one=False, verbose=False):
        self.consumers = consumers
        self.producers = producers
        self.stores_in = stores_in
        self.stores_out = stores_out
        self.count = count
        self.timeout = timeout
        self.threads = threads
        self.sleep_period = sleep_period
        self.deduplicate = deduplicate
        self.filter_last_one = filter_last_one

        self.verbose = verbose

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
