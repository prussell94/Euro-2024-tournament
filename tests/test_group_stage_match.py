from unittest import TestCase
from teams.team import Team
from matches.performance_strategies.distribution_strategy import DistributionStrategy
from matches.performance_strategies.ml_model_strategy import MLModelStrategy
from teams.quality_distribution import QualityDistribution
from matches.group_stage_match import GroupStageMatch
import pandas as pd
from matches.bayesian import BayesianNN
import torch.nn as nn
import torch.nn.functional as F
import torchbnn
import torch
import random
import numpy as np

class TestGroupStageMatch(TestCase):
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

    def test_group_stage_game_winner_distribution_strategy(self):
        strategy = DistributionStrategy()

        team_a_offensive_distribution = QualityDistribution(.8, .7, seed=1)
        team_a_defensive_distribution = QualityDistribution(2.1, .7, seed=1)

        team_b_offensive_distribution = QualityDistribution(2.1, .7, seed=1)
        team_b_defensive_distribution = QualityDistribution(1.4, .5, seed=1)

        team_a = Team('Albania', team_a_offensive_distribution, team_a_defensive_distribution)
        team_b = Team('Belgium', team_b_offensive_distribution, team_b_defensive_distribution)

        group_stage_match = GroupStageMatch(team_a, team_b, strategy=strategy)

        match = group_stage_match.simulate_match(team_a, team_b, strategy)

        expected_goals_a = 1
        expected_goals_b = 2

        expected_points_a = 0
        expected_points_b = 3

        self.assertEqual(expected_goals_a, match.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match.get_teamBGoalsScored())

        self.assertEqual(expected_points_a, match.get_teamA().get_pointsEarned())
        self.assertEqual(expected_points_b, match.get_teamB().get_pointsEarned())

    def test_group_stage_game_draw_distribution_strategy(self):
        strategy = DistributionStrategy()

        team_a_offensive_distribution = QualityDistribution(1.2, .7, seed=1)
        team_a_defensive_distribution = QualityDistribution(1.2, .7, seed=1)

        team_b_offensive_distribution = QualityDistribution(1.1, .7, seed=1)
        team_b_defensive_distribution = QualityDistribution(1.4, .5, seed=1)

        team_a = Team('Croatia', team_a_offensive_distribution, team_a_defensive_distribution)
        team_b = Team('Italy', team_b_offensive_distribution, team_b_defensive_distribution)

        group_stage_match = GroupStageMatch(team_a, team_b, strategy=strategy)

        match = group_stage_match.simulate_match(team_a, team_b, strategy)

        expected_goals_a = 1
        expected_goals_b = 1

        expected_points_a = 1
        expected_points_b = 1

        self.assertEqual(expected_goals_a, match.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match.get_teamBGoalsScored())

        self.assertEqual(expected_points_a, match.get_teamA().get_pointsEarned())
        self.assertEqual(expected_points_b, match.get_teamB().get_pointsEarned())

    def test_group_stage_game_winner_bnn_model_strategy(self):
        self.set_seed(1)

        strategy = MLModelStrategy(self.euro_squads, ml_model=self.bnn_model)

        team_a_offensive_distribution = QualityDistribution(.8, .7, seed=1)
        team_a_defensive_distribution = QualityDistribution(2.1, .7, seed=1)

        team_b_offensive_distribution = QualityDistribution(2.1, .7, seed=1)
        team_b_defensive_distribution = QualityDistribution(1.4, .5, seed=1)

        team_a = Team('Albania', team_a_offensive_distribution, team_a_defensive_distribution)
        team_b = Team('Belgium', team_b_offensive_distribution, team_b_defensive_distribution)

        group_stage_match = GroupStageMatch(team_a, team_b, strategy=strategy)

        match = group_stage_match.simulate_match(team_a, team_b, strategy)

        expected_goals_a = 1
        expected_goals_b = 0

        expected_points_a = 3
        expected_points_b = 0

        self.assertEqual(expected_goals_a, match.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match.get_teamBGoalsScored())

        self.assertEqual(expected_points_a, match.get_teamA().get_pointsEarned())
        self.assertEqual(expected_points_b, match.get_teamB().get_pointsEarned())
        

        
