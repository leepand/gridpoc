from abc import abstractmethod, ABCMeta
from Arthur.core.utils.entities.ViewType import ViewType


class AbstractStore:
    """
    Abstract class for Backend Storage
    This class will define API interface for front ends to connect with various types of backends
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Empty constructor for now. This is deliberately not marked as abstract, else every
        derived class would be forced to create one.
        """
        pass