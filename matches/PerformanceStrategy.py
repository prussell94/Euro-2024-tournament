from abc import ABC, abstractmethod

class PerformanceStrategy(ABC):
    @abstractmethod
    def predict_goals(self, team, opponent):
        pass