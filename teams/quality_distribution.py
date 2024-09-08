from scipy.stats import norm, truncnorm
import numpy as np

class QualityDistribution():
    LOWER_BOUND_GOALS = 0  # Equivalent to `private static final`
    UPPER_BOUND_GOALS = 6  # Equivalent to `private static final`

    """
    A class representing a probability distribution which reflects the quality of a certain component of a team (offensive, defensive quality etc.)

    Attributes:
        mean (float): The mean of quality
        stdev (float): The standard deviation of quality.
    """
    def __init__(self, mean, stdev, seed=None):
        self._mean = mean
        self._stdev = stdev
        if seed is not None:
            self.random_state = np.random.default_rng(seed)  # Create a seeded random generator
        else:
            self.random_state = None  # No seeding, random by default

    def get_mean(self):
        return self._mean
    def get_stdev(self):
        return self._stdev
    
    @property
    def mean(self):
        return self._mean
    
    @property
    def stdev(self):
        return self._stdev

    @mean.setter
    def mean(self, m):
        self._mean = m

    @stdev.setter
    def stdev(self, std):
        self._stdev = std

    def get_goal_estimate(self):
        """
        Retrieves an estimate of number of goals scored/conceded

        Returns:
            number_of_goals (float): An estimate of number of goals scored/conceded. Currently upper bounded with 6 goals
        """
        lower_bound=QualityDistribution.LOWER_BOUND_GOALS
        upper_bound=QualityDistribution.UPPER_BOUND_GOALS

        a = (lower_bound - self.get_mean() / self.get_stdev())
        b = (upper_bound - self.get_mean()) / self.get_stdev()
        team_dist=truncnorm(a=a, b=b, loc=self.get_mean(), scale=self.get_stdev())
        number_of_goals = team_dist.rvs(size=1,random_state=self.random_state)
        return number_of_goals[0]
    
    def accept(self, visitor):
        return visitor.visit_quality_distribution(self)