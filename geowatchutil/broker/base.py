import time


class GeoWatchBroker(object):

    verbose = False

    threads = None
    sleep_period = None
    deduplicate = False
    count = 1
    timeout = 5

    # Streaming Data
    consumers = None
    producers = None

    # Batch Storage
    stores_in = None
    stores_out = None

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
                    print str(len(messages_out))+" unique messages out of "+str(len(messages_out))+" messages."
            else:
                messages_out = messages_all

            if messages_out:

                if self.producers:
                    for producer in self.producers:
                        producer.send_messages(messages_out)

                if self.stores_out:
                    for store in self.stores_out:
                        store.write_messages(messages_out, flush=True)

            self._post(messages=messages_out)

            if max_cycle > 0 and cycle == max_cycle:
                break

            cycle += 1
            time.sleep(self.sleep_period)

    def __init__(self, consumers=None, producers=None, stores_in=None, stores_out=None, count=1, timeout=5, threads=1, sleep_period=5, deduplicate=False, verbose=False):
        self.consumers = consumers
        self.producers = producers
        self.stores_in = stores_in
        self.stores_out = stores_out
        self.count = count
        self.timeout = timeout
        self.threads = threads
        self.sleep_period = sleep_period
        self.deduplicate = False

        self.verbose = verbose
