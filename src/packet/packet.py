## @file packet.py
# @brief Contains definition for the Packet class.
# @author Guy Chamberlain-Webber

import src.constants as constants

from src.packet.content import Content
from src.packet.headers import BaseHeader
from src.packet.readable import IReadable
from src.packet.serial_data_transfer import SerialDataTransfer
from src.packet.writable import IWritable


## Increments the sequence number.
#
# Once the sequence number becomes greater than the
# max sequence number (15), it will wrap back round to zero.
def increment_seq():
    Packet.seq += 1

    if Packet.seq > constants.SEQ_WRAP:
        Packet.seq = 0x01


## Provides an abstraction of a data packet, which will be able to be transmitted to, and received
# from the panel.
class Packet(Content, IWritable, IReadable):
    seq = 0x01  # Sequence number

    def __init__(self, header: BaseHeader, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(header, BaseHeader):
            raise AttributeError(f"'{type(header)}' is not of expected type, BaseHeader.")

        self._header = header

        # Combine parameters of header and kwargs together
        _params_copy = self._params
        self._params = header.get_parameters()
        self._params.update(_params_copy)

        # Update packet length
        self.set_parameter("packet_length", len(self._params))

    ## Gets an object as an array of bytes.
    #
    # The packet will provide SOH and SEQ numbers to the byte array, as well
    # as a checksum at the end based on all previous bytes.
    #
    # @return The containing object as an array of bytes.
    def get_byte_array(self) -> list:
        default_array = super().get_byte_array()

        default_array.insert(0, Packet.seq)

        checksum = 0
        for byte in default_array:
            checksum += byte

        # Modulus operation to ensure checksum can be contained within one byte.
        checksum %= 256

        default_array.insert(0, constants.SOH)
        default_array.append(checksum)

        return default_array

    ## Writes to a serial communications port.
    def write(self):
        serial = SerialDataTransfer()

        data = self.get_byte_array()
        serial.write(data)

        increment_seq()

        serial.__del__()

    ## Reads from a serial communication port.
    #
    # The data read (if any) from the communication port.
    def read(self, size: int) -> list:
        serial = SerialDataTransfer()
        has_data = False
        read_data = bytes

        while not has_data:
            read_data = serial.read(size)

            if read_data is None:
                # No data could be read so try another packet.
                serial.__del__()
                self.write()
                serial = SerialDataTransfer()
            elif len(read_data) > 1:
                # Data has been found.
                has_data = True

        # If data has been read, we should send back an acknowledgement (ACK) byte,
        # so we will longer receive data.
        if read_data:
            serial.write_byte(constants.ACK)

        return list(read_data)
