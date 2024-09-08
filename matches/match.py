import pandas as pd
from abc import ABC, abstractmethod
import numpy as np

class Match(ABC):
    """
    A class representing a soccer match

    Attributes:
        teamA (Team): The first team in the mathch.
        teamB (Team): The second team in the match.
        team_a_goals_scored (int): The number of goals scored by first team.
        team_b_goals_scored (int): The number of goals scored by second team.
    """
    def __init__(self, teamA=None, teamB=None, gameId='', nextGameId='', team_a_goals_scored=0, team_b_goals_scored=0, winner=None, strategy=None):
        """
        Initialize a new match instance.

        Args:
            teamA (Team): The first team in the match.
            teamB (Team): The second team in the match.
            team_a_goals_scored (int): The number of goals scored by first team.
            team_b_goals_scored (int): The number of goals scored by second team.
        """
        self._teamA = teamA
        self._teamB = teamB
        self._game_id = gameId
        self._next_game_id = nextGameId
        self._teamAGoalsScored = team_a_goals_scored
        self._teamBGoalsScored = team_b_goals_scored
        self._winner = winner
        self._strategy = strategy
        self._gameEndsAt = None

    @property
    def teamA(self):
        return self._teamA

    @property
    def teamB(self):
        return self._teamB
    
    @property
    def game_id(self):
        return self._gameId

    @property
    def next_game_id(self):
        return self._nextGameId

    @property
    def team_a_goals_scored(self):
        return self._teamAGoalsScored

    @property
    def team_b_goals_scored(self):
        return self._teamBGoalsScored
    
    @property
    def winner(self):
        return self._winner

    @teamA.setter
    def teamA(self, teamA):
        self._teamA = teamA

    @teamB.setter
    def teamB(self, teamB):
        self._teamB = teamB

    @game_id.setter
    def gameId(self, gameId):
        self._gameId = gameId
    
    @next_game_id.setter
    def next_game_id(self, nextGameId):
        self._nextGameId = nextGameId

    @team_a_goals_scored.setter
    def team_a_goals_scored(self, teamAGoalsScored):
        self._teamAGoalsScored = teamAGoalsScored

    @team_b_goals_scored.setter
    def team_b_goals_scored(self, teamBGoalsScored):
        self._teamBGoalsScored = teamBGoalsScored

    @winner.setter
    def winner(self, winning_team):
        self._winner = winning_team

    def get_teamA(self):
        return self._teamA
    def get_teamB(self):
        return self._teamB
    def get_gameId(self):
        return self._gameId
    def get_nextGameId(self):
        return self._nextGameId
    def get_teamAGoalsScored(self):
        return self._teamAGoalsScored
    def get_teamBGoalsScored(self):
        return self._teamBGoalsScored
    def get_winner(self):
        return self._winner    
    def get_game_ends_at(self):
        """
        Get the value of gameEndsAt.
        
        Returns:
            str: The time when the game was won.
        """
        return self._gameWonWhen   
  
    def set_teamA(self, teamA):
        self._teamA = teamA
    def set_teamB(self, teamB):
        self._teamB = teamB
    def set_gameId(self, gameId):
        self._gameId = gameId
    def set_nextGameId(self, nextGameId):
        self._nextGameId = nextGameId
    def set_teamAGoalsScored(self, scored):
        self._teamAGoalsScored = scored
    def set_teamBGoalsScored(self, scored):
        self._teamBGoalsScored = scored
    def addToAGoalsScored(self, scored):
        self._teamAGoalsScored = self._teamAGoalsScored+scored
    def addToBGoalsScored(self, scored):
        self._teamBGoalsScored = self._teamBGoalsScored+scored
    def set_winner(self, winner):
        self._winner = winner
    def set_game_ends_at(self, time_frame):
        """
        Set the gameWonWhen attribute, indicating when the game was won.
        
        Args:
            time_frame (str): The time when the game was won ('90 minutes', '120 minutes', 'penalty kicks').
        """
        self._gameWonWhen = time_frame
    
    def simulate_match(self, team_a, team_b, strategy, seed=0):
        match = strategy.calculate_performance(team_a, team_b)

        team_a_goals_scored = match.get_teamAGoalsScored()
        team_b_goals_scored = match.get_teamBGoalsScored()

        team_a_goals_scored_rounded = np.round(team_a_goals_scored)
        team_b_goals_scored_rounded = np.round(team_b_goals_scored)

        team_a.set_goalsScored(team_a_goals_scored_rounded)
        team_a.set_goalsConceded(team_b_goals_scored_rounded)

        team_b.set_goalsScored(team_b_goals_scored_rounded)
        team_b.set_goalsConceded(team_a_goals_scored_rounded)

        match = self.simulate_match_impl(team_a, team_b, strategy)
        # match = Match(team_a, team_b, team_a_goals_scored=team_a_goals_scored, team_b_goals_scored=team_b_goals_scored)
        return match

    def simulate_match_impl(self, team_a, team_b, strategy, seed=0):
        pass
    
    def simulate_match_with_metrics(self, team_a, team_b):
        """
        Simulate match with metrics derived from aggregated FIFA ratings

        Args:
            team_a (Team): first team
            team_b (Team): second team

        Returns:
            match (Match): The match object which includes teams and scoreline
        """
        """retrieve the quality metrics for each team, check that they are in the correct order and then
        combine them for each team (need team and opposition metrics). Modify them into tensors so that
        they can be inputted into the model and output the estimated number of goals. This means that
        the whole averaging of goals scored/conceded does not occur. 
        """

        quality_columns = ['overall', 'potential', 'pace', 'shooting', 'passing', 'dribbling',
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
        
        player_count_df = euro_2024_squads.groupby("nationality_name")['player_id'].count()

        agg_quality_df = euro_2024_squads.groupby(['nationality_name'])[quality_columns].mean()
        
        team_a_quality = team_a.quality_metrics
        team_b_quality = team_b.quality_metrics

        combined_df = pd.merge(agg_quality_df, player_count_df, left_on="nationality_name", right_on="nationality_name").rename(columns={"player_id": "player_count"})
        
        team_b = pd.concat([combined_df.iloc[2, :-1], combined_df.iloc[0, :-1], combined_df.iloc[2, -1:]])
        team_a = pd.concat([combined_df.iloc[0, :-1], combined_df.iloc[2, :-1], combined_df.iloc[0, -1:]])
        pd.concat([team_a_quality, team_b_quality], )

    # def simulate_match(self, team_a, team_b, strategy):
        
    #     # this method will calculate the performance independent of what type of match it is (knockout, group stage)
    #     strategy.calculate_performance(team_a, team_b)

    #     # this method will be implemented differently based off what type of match it is
    #     return self.calculate_performance_impl(team_a, team_b, strategy)

    # def calculate_performance_impl(team_a, team_b, strategy):
    #     pass

    def simulateMatch(self, team_a, team_b):
        """
        Simulates match

        Args:
            team_a (Team): first team
            team_b (Team): second team

        Returns:
            match (Match): The match object which includes teams and scoreline
        """
        team_a_goals_scored = team_a.get_offensiveQualityDistribution().get_goal_estimate()[0]
        team_a_goals_conceded = team_a.get_defensiveQualityDistribution().get_goal_estimate()[0]
        team_b_goals_scored = team_b.get_offensiveQualityDistribution().get_goal_estimate()[0]
        team_b_goals_conceded = team_b.get_defensiveQualityDistribution().get_goal_estimate()[0]

        team_a_goals_scored_avg = (team_a_goals_scored+team_b_goals_conceded)/2
        team_b_goals_scored_avg = (team_b_goals_scored+team_a_goals_conceded)/2
    
        points_distribution = self.points_awarded(team_a_goals_scored_avg, team_b_goals_scored_avg)
    
        team_a_goals_scored = round(team_a_goals_scored_avg, 0)
        team_b_goals_scored = round(team_b_goals_scored_avg, 0)

        points_distribution = self.points_awarded(team_a_goals_scored, team_b_goals_scored)
        team_a.set_goalsScored(team_a_goals_scored)
        team_a.set_goalsConceded(team_b_goals_scored)
        team_a.set_pointsEarned(points_distribution[0])

        team_b.set_goalsScored(team_b_goals_scored)
        team_b.set_goalsConceded(team_a_goals_scored)
        team_b.set_pointsEarned(points_distribution[1])
    
        return Match(team_a, team_b, team_a_goals_scored, team_b_goals_scored)
    
    def simulateMatchWithModel(self, team_a, team_b):
        """
        Simulates match

        Args:
            team_a (Team): first team
            team_b (Team): second team

        Returns:
            match (Match): The match object which includes teams and scoreline
        """
        
        team_a_goals_scored, team_b_goals_scored = self.match_simulator.simulate_match(team_a.get_countryName(), team_b.get_countryName())

        team_a_goals_scored = round(team_a_goals_scored, 0)
        team_b_goals_scored = round(team_b_goals_scored, 0)

        points_distribution = self.points_awarded(team_a_goals_scored, team_b_goals_scored)
        team_a.set_goalsScored(team_a_goals_scored)
        team_a.set_goalsConceded(team_b_goals_scored)
        team_a.set_pointsEarned(points_distribution[0])

        team_b.set_goalsScored(team_b_goals_scored)
        team_b.set_goalsConceded(team_a_goals_scored)
        team_b.set_pointsEarned(points_distribution[1])
    
        return Match(team_a, team_b, team_a_goals_scored, team_b_goals_scored)