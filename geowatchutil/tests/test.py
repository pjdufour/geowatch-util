import unittest
from geowatchutil.buffer.base import GeoWatchBuffer
from geowatchutil.broker.base import GeoWatchBroker
from geowatchutil.store.geowatch_store_file import GeoWatchStoreFile
from geowatchutil.channel.base import GeoWatchChannelError
from geowatchutil.channel.geowatch_channel_slack import GeoWatchChannelSlack


class TestBuffer(unittest.TestCase):

    def test_buffer_clear(self):
        b = GeoWatchBuffer(limit=3)
        b.add_message("a")
        b.add_message("b")
        b.add_message("c")
        b.clear()
        self.assertTrue(b.empty())

    def test_buffer_full(self):
        b = GeoWatchBuffer(limit=2)
        b.add_message("a")
        b.add_message("b")
        b.add_message("c")
        self.assertTrue(b.full())


class TestBroker(unittest.TestCase):

    def test_broker_plain(self):
        m_in = ["hello", "world"]
        outfile = "out.txt"
        store_out = GeoWatchStoreFile(outfile, "GeoWatchCodecPlain", which="first", which_index="0")
        stores_out = [store_out]
        broker = GeoWatchBroker(
            stores_out=stores_out,
            verbose=True)
        broker.receive_messages(m_in)
        m_out = ""
        with open(outfile, 'rb') as f:
            m_out = f.read()
        self.assertEqual(m_out, "hello\nworld")

    def test_broker_json(self):
        m_in = {"hello": "world"}
        outfile = "out.json"
        store_out = GeoWatchStoreFile(outfile, "GeoWatchCodecJSON", which="first", which_index="0")
        stores_out = [store_out]
        broker = GeoWatchBroker(
            stores_out=stores_out,
            verbose=True)
        broker.receive_message(m_in)
        m_out = ""
        with open(outfile, 'rb') as f:
            m_out = f.read()
        self.assertEqual(m_out, "{\"hello\":\"world\"}")


class TestChannel(unittest.TestCase):

    def test_channel_slack(self):
        with self.assertRaises(GeoWatchChannelError):
            GeoWatchChannelSlack.decode(1)

        c = GeoWatchChannelSlack()
        with self.assertRaises(GeoWatchChannelError):
            c.get_messages_raw(1)

if __name__ == '__main__':
    unittest.main()