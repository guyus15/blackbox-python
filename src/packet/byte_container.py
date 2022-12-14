## @file byte_container.py
# @brief Contains interface IByteContainer used to enforce the presence specific byte-related functions
# inside a class.
# @author Guy Chamberlain-Webber

import abc


## An interface containing specific byte-related functions.
class IByteContainer(abc.ABC):
    ## Gets an object as an array of bytes.
    #
    # @return The containing object as an array of bytes.
    @abc.abstractmethod
    def get_byte_array(self) -> list:
        pass

    # Sets the parameter contained at 'key' to 'value'.
    @abc.abstractmethod
    def set_parameter(self, key: str, value):
        pass

    # Gets the parameter contained at 'key'
    #
    # @return The parameter contained at the specified key.
    @abc.abstractmethod
    def get_parameter(self, key: str):
        pass

    ## Gets all the content parameters
    #
    # @return The parameters of the content object.
    @abc.abstractmethod
    def get_parameters(self) -> dict:
        pass
