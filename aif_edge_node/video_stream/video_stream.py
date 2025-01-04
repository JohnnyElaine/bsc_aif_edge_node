from abc import ABC, abstractmethod

class VideoStream(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass