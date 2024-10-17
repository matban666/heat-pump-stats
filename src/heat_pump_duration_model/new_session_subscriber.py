from abc import ABC, abstractmethod

class NewSessionSubscriber(ABC):
    """
    Abstract class for new session subscribers

    Classes that inherit from this can be notified when a new session is created
    """
    @abstractmethod
    def new_session_update(self, session):
        """
        Abstract method to be implemented by the subscriber
        It is called when a new session is created
        """
        raise NotImplementedError