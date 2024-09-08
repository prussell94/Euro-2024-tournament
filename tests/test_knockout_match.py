
from unittest import TestCase
from teams.team import Team
from matches.performance_strategies.distribution_strategy import DistributionStrategy
from teams.quality_distribution import QualityDistribution
from matches.knockout_match import KnockoutMatch

class TestKnockoutMatch(TestCase):
    def test_knockout_match_in_regulation(self):
        strategy = DistributionStrategy()
        
        team_a_offensive_distribution = QualityDistribution(.8, .2, seed=80)
        team_a_defensive_distribution = QualityDistribution(2.1, .1, seed=80)

        team_b_offensive_distribution = QualityDistribution(2.1, .2, seed=80)
        team_b_defensive_distribution = QualityDistribution(1.1, .1, seed=80)

        team_a = Team('Albania', team_a_offensive_distribution, team_a_defensive_distribution)
        team_b = Team('Belgium', team_b_offensive_distribution, team_b_defensive_distribution)

        knockout_match = KnockoutMatch(team_a, team_b, strategy=strategy)

        match = knockout_match.simulate_match(team_a, team_b, strategy)

        expected_goals_a = 1
        expected_goals_b = 2
        expected_end_of_game = "90"

        self.assertEqual(expected_goals_a, match.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match.get_teamBGoalsScored())
        self.assertEqual(expected_end_of_game, match.get_game_ends_at())

    def test_knockout_match_in_ot(self):
        strategy = DistributionStrategy()
        
        team_a_offensive_distribution = QualityDistribution(1.8, .5, seed=71)
        team_a_defensive_distribution = QualityDistribution(2.1, .5, seed=71)

        team_b_offensive_distribution = QualityDistribution(1.1, .5, seed=71)
        team_b_defensive_distribution = QualityDistribution(1.1, .5, seed=71)

        team_a = Team('Albania', team_a_offensive_distribution, team_a_defensive_distribution)
        team_b = Team('Belgium', team_b_offensive_distribution, team_b_defensive_distribution)

        knockout_match = KnockoutMatch(team_a, team_b, strategy=strategy)

        match = knockout_match.simulate_match(team_a, team_b, strategy, seed=12)

        expected_goals_a = 1
        expected_goals_b = 2
        expected_end_of_game = "120"

        self.assertEqual(expected_goals_a, match.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match.get_teamBGoalsScored())
        self.assertEqual(expected_end_of_game, match.get_game_ends_at())

    # def test_knockout_match_in_pk(self):
    #     strategy = DistributionStrategy()
        
    #     team_a_offensive_distribution = QualityDistribution(1.8, .5, seed=80)
    #     team_a_defensive_distribution = QualityDistribution(2.1, .5, seed=80)

    #     team_b_offensive_distribution = QualityDistribution(1.1, .5, seed=80)
    #     team_b_defensive_distribution = QualityDistribution(1.1, .5, seed=80)

    #     team_a = Team('Albania', team_a_offensive_distribution, team_a_defensive_distribution)
    #     team_b = Team('Belgium', team_b_offensive_distribution, team_b_defensive_distribution)

    #     knockout_match = KnockoutMatch(team_a, team_b, strategy=strategy)

    #     match = knockout_match.simulate_match(team_a, team_b, strategy)

    #     expected_goals_a = 2
    #     expected_goals_b = 3
    #     expected_end_of_game = "pk"

    #     self.assertEqual(expected_goals_a, match.get_teamAGoalsScored())
    #     self.assertEqual(expected_goals_b, match.get_teamBGoalsScored())
    #     self.assertEqual(expected_end_of_game, match.get_game_ends_at())