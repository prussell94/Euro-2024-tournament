from unittest import TestCase
from matches.performance_strategies.ml_model_strategy import MLModelStrategy
from matches.match import Match
from teams.team import Team
import pandas as pd
from matches.bayesian import BayesianNN
import torch.nn as nn
import torch.nn.functional as F
import torchbnn
import torch
import random
import numpy as np
    
class TestMLModelStrategy(TestCase):
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
    
    def test_ml_model_strategy_success(self):
        self.set_seed(42)  # Set seed to any integer you prefer

        strategy = MLModelStrategy(self.euro_squads, ml_model=self.bnn_model)

        team_a_name = "Albania"
        team_b_name = "Belgium"

        match_with_ml_strategy = strategy.calculate_performance(team_a_name, team_b_name)

        expected_goals_a = 0
        expected_goals_b = 3

        self.assertEqual(expected_goals_a, match_with_ml_strategy.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match_with_ml_strategy.get_teamBGoalsScored())

    def test_ml_model_strategy_draw_success(self):
        
        self.set_seed(11)

        strategy = MLModelStrategy(self.euro_squads, ml_model=self.bnn_model)

        team_a_name = "England"
        team_b_name = "France"

        match_with_ml_strategy = strategy.calculate_performance(team_a_name, team_b_name)

        expected_goals_a = 0
        expected_goals_b = 0

        self.assertEqual(expected_goals_a, match_with_ml_strategy.get_teamAGoalsScored())
        self.assertEqual(expected_goals_b, match_with_ml_strategy.get_teamBGoalsScored())