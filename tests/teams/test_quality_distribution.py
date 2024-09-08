from unittest import TestCase
import random
from teams.quality_distribution import QualityDistribution


class TestQualityDistribution(TestCase):
    def test_distribution(self):
        distribution = QualityDistribution(2, .5, seed=42)
        number_of_goals = distribution.get_goal_estimate()

        # Assert based on expected value with the seed
        self.assertAlmostEqual(number_of_goals, 2.37598127146115)  # Use expected value based on the seed