from rich.console import Console
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats

def create_table():
    table = Table(title="Players from FIN")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Team", style="magenta")
    table.add_column("Goals", justify="right", style="green")
    table.add_column("Assists", justify="right", style="blue")
    table.add_column("Points", justify="right", style="bold yellow")
    return table

def add_players_to_table(table, players):
    for player in players:
        points = player.goals + player.assists
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(points)
        )

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality("FIN")
    console = Console()
    table = create_table()
    add_players_to_table(table, players)
    console.print(table)

if __name__ == "__main__":
    main()
