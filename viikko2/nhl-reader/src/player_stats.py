class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = self.reader.get_players()
        filtered_players = [p for p in players if p.nationality == nationality]
        sorted_players = sorted(filtered_players, key=lambda p: p.goals + p.assists, reverse=True)
        return sorted_players
