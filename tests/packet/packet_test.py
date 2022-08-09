## @file packet_test.py
# @brief Contains tests to test the 'packet' file and class.
# @author Guy Chamberlain-Webber

import unittest
from src.packet.packet import Packet
from src.packet.headers import LocalHeaderMX5, LocalHeaderMX6
from src.packet.packet_ids import PacketID

this_packet = None


## This test case tests the 'packet' file and class.
class TestPacket(unittest.TestCase):
    def setUp(self) -> None:
        global this_packet

        header = LocalHeaderMX5(PacketID.INVALID)

        this_packet = Packet(
            header,
            value1=1,
            value2=2,
            value3=3
        )

    # Test 1
    def test_mx5_packet_size(self):
        # This test ensures that the size of a packet with a header type of MX Speak 5 with no
        # contents will be 9.

        header = LocalHeaderMX5(PacketID.INVALID)
        mx5_packet = Packet(header)

        self.assertEqual(len(mx5_packet._params), 9)

    # Test 2
    def test_mx6_packet_size(self):
        # This test ensures that the size of a packet with a header type of MX Speak 6 with no
        # contents will be 11.

        header = LocalHeaderMX6(PacketID.NET_VERSION_REQUEST)
        mx6_packet = Packet(header)

        self.assertEqual(len(mx6_packet._params), 11)

    # Test 3
    # noinspection PyUnresolvedReferences
    def test_packet_contents(self):
        # This test ensures that the constructor of the Packet class behaves as expected by correctly merging
        # together the parameters of the header and contents.

        global this_packet

        expected_contents = [0x01, 0x01, 0x09,
                             0x00, 0x00, 0x00,
                             0x00, 0x00, 0x00,
                             0x00, 0x00, 0x01,
                             0x02, 0x03, 0x0f]

        self.assertEqual(this_packet.get_byte_array(), expected_contents)
