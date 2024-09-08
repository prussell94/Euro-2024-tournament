
from unittest import TestCase
from teams.team import Team
from matches.performance_strategies.distribution_strategy import DistributionStrategy
from teams.quality_distribution import QualityDistribution
from matches.knockout_match import KnockoutMatch
import pandas as pd
from matches.bayesian import BayesianNN
import torch.nn as nn
import torch.nn.functional as F
import torchbnn
import torch

class TestKnockoutMatch(TestCase):
    def setUp(self):
        self.euro_squads = pd.read_csv("matches/modified_euro_2024_squads_2.csv")
        self.bnn_model = BayesianNN()
        self.bnn_model.load_state_dict(torch.load('matches/bnn_model_state.pth'))
        self.bnn_model.eval()

    def set_seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

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

    def test_knockout_match_in_pk(self):
        strategy = DistributionStrategy()
        
        team_a_offensive_distribution = QualityDistribution(1.8, .5, seed=80)
        team_a_defensive_distribution = QualityDistribution(2.1, .5, seed=80)

        team_b_offensive_distribution = QualityDistribution(1.1, .5, seed=80)
        team_b_defensive_distribution = QualityDistribution(1.1, .5, seed=80)

        team_a = Team('Albania', team_a_offensive_distribution, team_a_defensive_distribution)
        team_b = Team('Belgium', team_b_offensive_distribution, team_b_defensive_distribution)

        knockout_match = KnockoutMatch(team_a, team_b, strategy=strategy)

        match = knockout_match.simulate_match(team_a, team_b, strategy)

        expected_goals_a = 3
        expected_goals_b = 2
        expected_end_of_game = "pk"

        self.assertEqual(expected_goals_a, match.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match.get_teamBGoalsScored())
        self.assertEqual(expected_end_of_game, match.get_game_ends_at())