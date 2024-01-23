from abc import ABC, abstractmethod

class Game(ABC):

    @abstractmethod
    def select_card(self, pos): pass

    @abstractmethod
    def move_card(self, pos): pass

    @abstractmethod
    def release_card(self, pos): pass