from unittest import TestCase
from matches.performance_strategies.distribution_strategy import DistributionStrategy
from matches.match import Match
from teams.team import Team
import random
from teams.quality_distribution import QualityDistribution

class TestDistributionStrategy(TestCase):
    def test_distribution_strategy_with_winner(self):
        strategy = DistributionStrategy()

        team_a_offensive_distribution = QualityDistribution(.8, .7, seed=1)
        team_a_defensive_distribution = QualityDistribution(2.1, .7, seed=1)

        team_b_offensive_distribution = QualityDistribution(2.1, .7, seed=1)
        team_b_defensive_distribution = QualityDistribution(1.4, .5, seed=1)

        team_a = Team('Albania', team_a_offensive_distribution, team_a_defensive_distribution)
        team_b = Team('Belgium', team_b_offensive_distribution, team_b_defensive_distribution)
        
        match_with_strategy = strategy.calculate_performance(team_a, team_b)

        expected_goals_a = 1
        expected_goals_b = 2

        self.assertEqual(expected_goals_a, match_with_strategy.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match_with_strategy.get_teamBGoalsScored())

    def test_distribution_strategy_with_draw(self):
        strategy = DistributionStrategy()

        team_a_offensive_distribution = QualityDistribution(1.2, .5, seed=1)
        team_a_defensive_distribution = QualityDistribution(1.2, .7, seed=1)

        team_b_offensive_distribution = QualityDistribution(1.1, .7, seed=1)
        team_b_defensive_distribution = QualityDistribution(1.4, .5, seed=1)

        team_a = Team('Croatia', team_a_offensive_distribution, team_a_defensive_distribution)
        team_b = Team('Italy', team_b_offensive_distribution, team_b_defensive_distribution)
        
        match_with_strategy = strategy.calculate_performance(team_a, team_b)

        expected_goals_a = 1
        expected_goals_b = 1

        self.assertEqual(expected_goals_a, match_with_strategy.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match_with_strategy.get_teamBGoalsScored())
