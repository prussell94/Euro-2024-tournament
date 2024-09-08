from matches.performance_strategies.performance_strategy import PerformanceStrategy
import numpy as np
import torch
import pickle
from scipy.stats import poisson
import pandas as pd
from matches.match import Match
import torch.nn as nn
import torch.nn.functional as F
import torchbnn

class BayesianNN(nn.Module):
    def __init__(self):
        super(BayesianNN, self).__init__()
        self.fc1 = torchbnn.BayesLinear(in_features=87, out_features=64, prior_mu=0.0, prior_sigma=0.1)
        self.fc2 = torchbnn.BayesLinear(in_features=64, out_features=32, prior_mu=0.0, prior_sigma=0.1)
        self.fc3 = torchbnn.BayesLinear(in_features=32, out_features=16, prior_mu=0.0, prior_sigma=0.1)
        self.fc4 = torchbnn.BayesLinear(in_features=16, out_features=1, prior_mu=0.0, prior_sigma=0.1)

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x), negative_slope=0.01)
        x = F.leaky_relu(self.fc2(x), negative_slope=0.01)
        x = F.leaky_relu(self.fc3(x), negative_slope=0.01)
        x = self.fc4(x)  # No activation function here for the final layer, as it's typically used for regression
        return x

class MLModelStrategy(PerformanceStrategy):
    def __init__(self, euro_2024_squads, ml_model):
        """
        Initialize a new match instance.

        Args:

        """
        self.euro_2024_squads = euro_2024_squads
        self._ml_model = ml_model
        self.quality_columns = ['overall', 'potential', 'pace', 'shooting', 'passing', 'dribbling',
                                'defending', 'physic', 'attacking_crossing', 'attacking_finishing',
                                'attacking_heading_accuracy', 'attacking_short_passing',
                                'attacking_volleys', 'skill_dribbling', 'skill_curve',
                                'skill_fk_accuracy', 'skill_long_passing', 'skill_ball_control',
                                'movement_acceleration', 'movement_sprint_speed', 'movement_agility',
                                'movement_reactions', 'movement_balance', 'power_shot_power',
                                'power_jumping', 'power_stamina', 'power_strength', 'power_long_shots',
                                'mentality_aggression', 'mentality_interceptions',
                                'mentality_positioning', 'mentality_vision', 'mentality_penalties',
                                'mentality_composure', 'defending_marking_awareness',
                                'defending_standing_tackle', 'defending_sliding_tackle',
                                'goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking',
                                'goalkeeping_positioning', 'goalkeeping_reflexes', 'goalkeeping_speed']
    
    def aggregate_quality_metrics(self):
        agg_quality_df = self.euro_2024_squads.groupby('nationality_name')[self.quality_columns].mean()
        return agg_quality_df
    
    def count_players_per_nationality(self):
        player_count_df = self.euro_2024_squads.groupby("nationality_name")['player_id'].count()
        return player_count_df

    def merge_quality_and_player_count(self, agg_quality_df, player_count_df):
        combined_df = pd.merge(agg_quality_df, player_count_df, left_on="nationality_name", right_on="nationality_name")
        combined_df = combined_df.rename(columns={"player_id": "player_count"})
        return combined_df
    
    def create_team_data(self, combined_df, team_a_name, team_b_name):

        if team_a_name == "Czechia":
            team_a_name = "Czech Republic"
        if team_b_name == "Czechia":
            team_b_name = "Czech Republic"
            
        team_a = combined_df[combined_df.reset_index()['nationality_name'] == team_a_name]
        team_b = combined_df[combined_df.reset_index()['nationality_name'] == team_b_name]

        print("team a")
        print(team_a_name)
        print(team_a)
        print(team_b)
        team_a_modified = pd.concat([team_a.iloc[0, 1:-1], team_b.iloc[0, 1:-1].add_suffix('_opposition'), team_a.iloc[0, -1:]])
        team_b_modified = pd.concat([team_b.iloc[0, 1:-1], team_a.iloc[0, 1:-1].add_suffix('_opposition'), team_b.iloc[0, -1:]])
        
        return team_a_modified, team_b_modified
    
    def make_predictions(self, team_a_data, team_b_data):
        
        ab = pd.concat([team_a_data, team_b_data], axis=1).transpose()
        ab = ab.apply(pd.to_numeric, errors='coerce')

        ab_tensor = torch.tensor(ab.values, dtype=torch.float32)
        
        output = self._ml_model(ab_tensor)
        predictions = output.squeeze()

        return predictions
    
    def calculate_poisson_probabilities(xg, max_goals=6):
        probabilities = [poisson.pmf(i, xg) for i in range(max_goals)]
        return probabilities
    
    def calculate_match_outcome_probabilities(self, xg_A, xg_B):
        max_goals = 6
        prob_A = self.calculate_poisson_probabilities(xg_A, max_goals)
        prob_B = self.calculate_poisson_probabilities(xg_B, max_goals)
    
        win_A = sum(p_A * sum(p_B for j, p_B in enumerate(prob_B) if j < i) for i, p_A in enumerate(prob_A))
        draw = sum(p_A * p_B for p_A, p_B in zip(prob_A, prob_B))
        win_B = sum(p_B * sum(p_A for j, p_A in enumerate(prob_A) if j < i) for i, p_B in enumerate(prob_B))
    
        total = win_A + draw + win_B
    
        return win_A / total, draw / total, win_B / total

    def simulate_match(self, team_a, team_b):

        agg_quality_df = self.aggregate_quality_metrics()
        player_count_df = self.count_players_per_nationality()
        combined_df = self.merge_quality_and_player_count(agg_quality_df, player_count_df)

        team_a_name = team_a.get_countryName()
        team_b_name = team_b.get_countryName()
        
        team_a, team_b = self.create_team_data(combined_df.reset_index(), team_a_name, team_b_name)
        predictions = self.make_predictions(team_a, team_b)

        if np.isnan(predictions[0].detach().numpy()) or predictions[0].detach().numpy() < 0:
            xg_team1 = np.random.poisson(0)  
        else:
            xg_team1 = np.random.poisson(predictions[0].detach().numpy())  

        if np.isnan(predictions[1].detach().numpy()) or predictions[1].detach().numpy() < 0:
            xg_team2 = np.random.poisson(0)  
        else:
            xg_team2 = np.random.poisson(predictions[1].detach().numpy()) 
    
        preds = [xg_team1, xg_team2]

        print("simulating game ")
        print(preds)

        return preds

    def calculate_performance(self, team_a, team_b):
        team_a_goals_scored, team_b_goals_scored = self.simulate_match(team_a, team_b)

        return Match(team_a, team_b, team_a_goals_scored=team_a_goals_scored, team_b_goals_scored=team_b_goals_scored)
    