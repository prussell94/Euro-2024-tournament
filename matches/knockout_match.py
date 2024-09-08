from matches.match import Match 
import random 

class KnockoutMatch(Match):
    def simulate_match_impl(self, team_a, team_b, strategy, seed=0):

        team_a_goals_scored_90 = team_a.get_goalsScored()
        team_b_goals_scored_90 = team_b.get_goalsScored()

        team_a_goals_scored = team_a_goals_scored_90
        team_b_goals_scored = team_b_goals_scored_90

        new_match = Match()

        random.seed(seed)

        if(team_a_goals_scored_90 == team_b_goals_scored_90):

            team_a_goals_OT, team_b_goals_OT = strategy.calculate_performance_get_goals(team_a, team_b)

            team_a_goals_OT = team_a_goals_OT/3
            team_b_goals_OT = team_b_goals_OT/3

            team_a_goals_scored_OT = round(team_a_goals_OT, 0)
            team_b_goals_scored_OT = round(team_b_goals_OT, 0) 

            team_a_goals_scored_120 = team_a_goals_scored_90 + team_a_goals_scored_OT
            team_b_goals_scored_120 = team_b_goals_scored_90 + team_b_goals_scored_OT

            if(team_a_goals_scored_120 != team_b_goals_scored_120):
                new_match.set_game_ends_at("120")
                team_a_goals_scored = team_a_goals_scored_120
                team_b_goals_scored = team_b_goals_scored_120

            elif(team_a_goals_scored_120 == team_b_goals_scored_120):
                new_match.set_game_ends_at("pk")
                kicker = 1
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

                    team_a_goals_scored = team_a_goals_scored_120 + 1
                    team_b_goals_scored = team_b_goals_scored_120

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
                            team_a_goals_scored_after_pk = team_a_goals_scored_120 + 1
                            team_b_goals_scored_after_pk = team_b_goals_scored_120

                            no_winner = False
                            team_a_goals_scored = team_a_goals_scored_after_pk
                            team_b_goals_scored = team_b_goals_scored_after_pk
                    
                        elif team_a_shooter_outcome < team_b_shooter_outcome:
                            team_b_goals_scored_after_pk = team_b_goals_scored_120 + 1
                            team_a_goals_scored_after_pk = team_a_goals_scored_120

                            no_winner = False
                            team_a_goals_scored = team_a_goals_scored_after_pk
                            team_b_goals_scored = team_b_goals_scored_after_pk

        else:
            new_match.set_game_ends_at("90")

        team_a.set_goalsScored(team_a_goals_scored)
        team_a.set_goalsConceded(team_b_goals_scored)

        team_b.set_goalsScored(team_b_goals_scored)
        team_b.set_goalsConceded(team_a_goals_scored)

        new_match.teamA = team_a
        new_match.teamB = team_b
        new_match.team_a_goals_scored = team_a_goals_scored
        new_match.team_b_goals_scored = team_b_goals_scored

        return new_match