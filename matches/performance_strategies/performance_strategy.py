from abc import ABC, abstractmethod
import random

class PerformanceStrategy(ABC):
    @abstractmethod
    def calculate_performance(self, team_a, team_b, seed):
        pass

    # @abstractmethod
    # def calculate_performance_impl(self, team_a_goals, team_b_goals):
    #     pass

    def calculate_performance_pk(self, team_a_goals_scored_120, team_b_goals_scored_120):

        choices = [0, 1]  
        weights = [0.2, 0.8]
        team_a_PK_score = 0
        team_b_PK_score = 0
            
        for r in range(1, 6):
            team_a_shooter_outcome =  random.choices(choices, weights=weights, k=1)[0]
            team_b_shooter_outcome =  random.choices(choices, weights=weights, k=1)[0]

            team_a_PK_score = team_a_PK_score + team_a_shooter_outcome
            team_b_PK_score = team_b_PK_score + team_b_shooter_outcome
            
        if(team_a_PK_score > team_b_PK_score):
            team_a_goals_scored_after_pk = team_a_goals_scored_120 + 1
            team_b_goals_scored_after_pk = team_b_goals_scored_120

            team_a_goals_scored = team_a_goals_scored_after_pk
            team_b_goals_scored = team_b_goals_scored_after_pk

        elif team_a_PK_score < team_b_PK_score:
            team_b_goals_scored_after_pk = team_b_goals_scored + 1
            team_a_goals_scored_after_pk = team_a_goals_scored

            team_a_goals_scored = team_a_goals_scored_after_pk
            team_b_goals_scored = team_b_goals_scored_after_pk
        else:
            
            no_winner = True
                    
            while(no_winner):
                team_a_shooter_outcome =  random.choices(choices, weights=weights, k=1)[0]
                team_b_shooter_outcome =  random.choices(choices, weights=weights, k=1)[0]

                if team_a_shooter_outcome > team_b_shooter_outcome:
                    team_a_goals_scored_after_pk = team_a_goals_scored + 1
                    team_b_goals_scored_after_pk = team_b_goals_scored

                    no_winner = False
                    team_a_goals_scored = team_a_goals_scored_after_pk
                    team_b_goals_scored = team_b_goals_scored_after_pk
                    
                elif team_a_shooter_outcome < team_b_shooter_outcome:
                    team_b_goals_scored_after_pk = team_b_goals_scored + 1
                    team_a_goals_scored_after_pk = team_a_goals_scored

                    no_winner = False
                    team_a_goals_scored = team_a_goals_scored_after_pk
                    team_b_goals_scored = team_b_goals_scored_after_pk

        return team_a_goals_scored, team_b_goals_scored