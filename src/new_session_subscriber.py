from abc import ABC, abstractmethod

class NewSessionSubscriber(ABC):
    @abstractmethod
    def new_session_update(self, session):
        pass