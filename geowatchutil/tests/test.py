import unittest
from geowatchutil.buffer.base import GeoWatchBuffer
from geowatchutil.broker.factory import build_broker
from geowatchutil.store.geowatch_store_file import GeoWatchStoreFile
from geowatchutil.channel.base import GeoWatchChannelError
from geowatchutil.channel.geowatch_channel_slack import GeoWatchChannelSlack
from geowatchutil.client.geowatch_client_slack import GeoWatchClientSlack


class TestBuffer(unittest.TestCase):
    """
    TestBuffer is used for testing GeoWatchBuffer
    """

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
        store_out = build_store(
            "file",
            outfile,
            "json",
            which="all",
            which_index="0"):
        stores_out = [store_out]
        broker = build_broker(
            "Test Name",
            "Test Description",
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
        store_out = build_store(
            "file",
            outfile,
            "json",
            which="first",
            which_index="0"):
        stores_out = [store_out]
        broker = build_broker(
            "Test Name",
            "Test Description",
            stores_out=stores_out,
            verbose=True)
        broker.receive_message(m_in)
        m_out = ""
        with open(outfile, 'rb') as f:
            m_out = f.read()
        self.assertEqual(m_out, "{\"hello\": \"world\"}")


class TestChannel(unittest.TestCase):

    def test_channel_slack(self):
        with self.assertRaises(GeoWatchChannelError):
            GeoWatchChannelSlack.decode(1)

        client = GeoWatchClientSlack()
        channel = GeoWatchChannelSlack(client, "random", "producer")
        with self.assertRaises(GeoWatchChannelError):
            channel.get_messages_raw(1)

if __name__ == '__main__':
    unittest.main()
