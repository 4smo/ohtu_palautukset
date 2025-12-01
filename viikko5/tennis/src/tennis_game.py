SCORE_NAMES = ["Love", "Fifteen", "Thirty", "Forty"]
POINTS_TO_WIN = 4


class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_score += 1
        else:
            self.player2_score += 1

    def _is_tie(self):
        return self.player1_score == self.player2_score

    def _get_tie_score(self):
        if self.player1_score >= 3:
            return "Deuce"
        return f"{SCORE_NAMES[self.player1_score]}-All"

    def _is_endgame(self):
        return self.player1_score >= POINTS_TO_WIN or self.player2_score >= POINTS_TO_WIN

    def _get_leader_name(self):
        if self.player1_score > self.player2_score:
            return self.player1_name
        return self.player2_name

    def _get_endgame_score(self):
        score_difference = abs(self.player1_score - self.player2_score)
        leader = self._get_leader_name()

        if score_difference == 1:
            return f"Advantage {leader}"
        return f"Win for {leader}"

    def _get_regular_score(self):
        player1_score_name = SCORE_NAMES[self.player1_score]
        player2_score_name = SCORE_NAMES[self.player2_score]
        return f"{player1_score_name}-{player2_score_name}"

    def get_score(self):
        if self._is_tie():
            return self._get_tie_score()
        elif self._is_endgame():
            return self._get_endgame_score()
        else:
            return self._get_regular_score()
