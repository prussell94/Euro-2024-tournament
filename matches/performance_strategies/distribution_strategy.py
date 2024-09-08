from matches.performance_strategies.performance_strategy import PerformanceStrategy
from matches.match import Match
import numpy as np
import random

class DistributionStrategy(PerformanceStrategy):
    def calculate_performance(self, team_a, team_b):

        team_a_goals_scored, team_b_goals_scored = self.calculate_performance_get_goals(team_a, team_b)

        # full_time_match = self.calculate_performance_impl(team_a.set_goalsScored(team_a_goals_scored), team_b.set_goalsScored(team_b_goals_scored))

        return Match(team_a, team_b, team_a_goals_scored=team_a_goals_scored, team_b_goals_scored=team_b_goals_scored)
    
    def calculate_performance_get_goals(self, team_a, team_b):

        offensive_quality_distribution_a = team_a.offensive_quality_distribution
        defensive_quality_distribution_a = team_a.defensive_quality_distribution

        offensive_quality_distribution_b = team_b.offensive_quality_distribution
        defensive_quality_distribution_b = team_b.defensive_quality_distribution

        team_a_goals_scored = offensive_quality_distribution_a.get_goal_estimate()
        team_a_goals_conceded = defensive_quality_distribution_a.get_goal_estimate()

        team_b_goals_scored = offensive_quality_distribution_b.get_goal_estimate()
        team_b_goals_conceded = defensive_quality_distribution_b.get_goal_estimate()

        team_a_goals_scored = (team_a_goals_scored+team_b_goals_conceded)/2
        team_b_goals_scored = (team_b_goals_scored+team_a_goals_conceded)/2

        print("team goals before rounding")
        print(team_a_goals_scored)
        return team_a_goals_scored, team_b_goals_scored
    
        # team_a_goals_scored_rounded = np.round(team_a_goals_scored)
        # team_b_goals_scored_rounded = np.round(team_b_goals_scored)

        # calculate_performance_impl(team_a_goals_scored_rounded, team_b_goals_scored_rounded)

        # if team_a_goals_scored_rounded > team_b_goals_scored_rounded:
        #     team_a_points_earned = 3
        #     team_b_points_earned = 0
        # elif team_a_goals_scored < team_b_goals_scored:
        #     team_b_points_earned = 3
        #     team_a_points_earned = 0
        # else:
        #     team_a_points_earned = 1
        #     team_b_points_earned = 1
        
        # team_a.set_pointsEarned(team_a_points_earned)
        # team_b.set_pointsEarned(team_b_points_earned)

        # return Match(team_a, team_b, team_a_goals_scored=team_a_goals_scored, team_b_goals_scored=team_b_goals_scored)
    
    # def calculate_performance_impl(self, team_a, team_b):
    #     team_a_goals_scored = team_a.get_goalsScored()
    #     team_b_goals_scored = team_b.get_goalsScored()

    #     team_a_goals_scored = np.round(team_a_goals_scored)
    #     team_b_goals_scored = np.round(team_b_goals_scored)

    #     full_time_match = Match(team_a, team_b, team_a_goals_scored=team_a_goals_scored, team_b_goals_scored=team_a_goals_scored)

    #     return full_time_match
    
    def calculate_performance_overtime(self, team_a, team_b):
        team_a_goals_scored, team_b_goals_scored = self.calculate_performance(team_a, team_b)
        team_a_goals_scored_ot, team_b_goals_scored_ot = team_a_goals_scored/3, team_b_goals_scored/3

        team_a_goals_scored_ot = np.round(team_a_goals_scored_ot)
        team_b_goals_scored_ot = np.round(team_b_goals_scored_ot)

        if(team_a_goals_scored_ot == team_b_goals_scored_ot):
            return Match(team_a, team_b, team_a_goals_scored=team_a_goals_scored+team_a_goals_scored_ot, team_b_goals_scored=team_b_goals_scored+team_b_goals_scored_ot)
        else:
            team_a_goals_scored, team_b_goals_scored = super().calculate_performance_pk(team_a_goals_scored_ot, team_b_goals_scored_ot)
            return Match(team_a, team_b, team_a_goals_scored=team_a_goals_scored, team_b_goals_scored=team_b_goals_scored)
        
    # def calculate_performance_pk(self, team_a_goals_scored_120, team_b_goals_scored_120):

    #     choices = [0, 1]  
    #     weights = [0.2, 0.8]
    #     team_a_PK_score = 0
    #     team_b_PK_score = 0
            
    #     for r in range(1, 6):
    #         team_a_shooter_outcome =  random.choices(choices, weights=weights, k=1)[0]
    #         team_b_shooter_outcome =  random.choices(choices, weights=weights, k=1)[0]

    #         team_a_PK_score = team_a_PK_score + team_a_shooter_outcome
    #         team_b_PK_score = team_b_PK_score + team_b_shooter_outcome
            
    #     if(team_a_PK_score > team_b_PK_score):
    #         team_a_goals_scored_after_pk = team_a_goals_scored_120 + 1
    #         team_b_goals_scored_after_pk = team_b_goals_scored_120

    #         team_a_goals_scored = team_a_goals_scored_after_pk
    #         team_b_goals_scored = team_b_goals_scored_after_pk

    #     elif team_a_PK_score < team_b_PK_score:
    #         team_b_goals_scored_after_pk = team_b_goals_scored + 1
    #         team_a_goals_scored_after_pk = team_a_goals_scored

    #         team_a_goals_scored = team_a_goals_scored_after_pk
    #         team_b_goals_scored = team_b_goals_scored_after_pk
    #     else:
            
    #         no_winner = True
                    
    #         while(no_winner):
    #             team_a_shooter_outcome =  random.choices(choices, weights=weights, k=1)[0]
    #             team_b_shooter_outcome =  random.choices(choices, weights=weights, k=1)[0]

    #             if team_a_shooter_outcome > team_b_shooter_outcome:
    #                 team_a_goals_scored_after_pk = team_a_goals_scored + 1
    #                 team_b_goals_scored_after_pk = team_b_goals_scored

    #                 no_winner = False
    #                 team_a_goals_scored = team_a_goals_scored_after_pk
    #                 team_b_goals_scored = team_b_goals_scored_after_pk
                    
    #             elif team_a_shooter_outcome < team_b_shooter_outcome:
    #                 team_b_goals_scored_after_pk = team_b_goals_scored + 1
    #                 team_a_goals_scored_after_pk = team_a_goals_scored

    #                 no_winner = False
    #                 team_a_goals_scored = team_a_goals_scored_after_pk
    #                 team_b_goals_scored = team_b_goals_scored_after_pk

    #     return team_a_goals_scored, team_b_goals_scored
        
