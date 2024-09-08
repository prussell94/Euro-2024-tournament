from matches.match import Match 

class GroupStageMatch(Match):
    def simulate_match_impl(self, team_a, team_b, strategy):
        
        points_distribution = self.points_awarded(team_a.get_goalsScored(), team_b.get_goalsScored())
            
        team_a.set_pointsEarned(points_distribution[0])
        team_b.set_pointsEarned(points_distribution[1])

        return Match(team_a, team_b, team_a_goals_scored=team_a.get_goalsScored(), team_b_goals_scored=team_b.get_goalsScored())
    
    def points_awarded(self, home_team_goals, away_team_goals):
        """
        Calculates points awarded based off number of goals scored for each team

        Args:
            home_team_goals (int): The number of goals scored by home team
            away_team_goals (int): The number of goals scored by away team

        Returns:
            home_team_points (int): The number of points awarded to home team
            away_team_points(int): The number of points awarded to away team
    
        Raises:
        ValueError: If home_team_goals or away_team_goals are negative.
        """
        if home_team_goals < 0:
            raise ValueError("goals for home team is not defined for negative numbers.")
        elif away_team_goals < 0:
            raise ValueError("goals for away team is not defined for negative numbers.")
        home_team_goals = round(home_team_goals, 0)
        away_team_goals = round(away_team_goals, 0)
        if(home_team_goals > away_team_goals):
            home_team_points = 3
            away_team_points = 0
        elif(home_team_goals == away_team_goals):
            home_team_points = 1
            away_team_points = 1
        else:
            home_team_points = 0
            away_team_points = 3
        return home_team_points, away_team_points