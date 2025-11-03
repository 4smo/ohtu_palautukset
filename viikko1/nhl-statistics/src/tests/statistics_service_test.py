import unittest
from statistics_service import StatisticsService, SortBy
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_loytyy_taysella_nimella(self):
        player = self.stats.search("Gretzky")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Gretzky")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.points, 124)

    def test_search_loytyy_osittaisella_nimella(self):
        player = self.stats.search("Kur")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Kurri")

    def test_search_ei_loydy(self):
        player = self.stats.search("Selanne")
        self.assertIsNone(player)

    def test_team_loytyy_useampi_pelaaja(self):
        players = self.stats.team("EDM")
        self.assertEqual(len(players), 3)
        names = [p.name for p in players]
        self.assertIn("Semenko", names)
        self.assertIn("Kurri", names)
        self.assertIn("Gretzky", names)

    def test_team_loytyy_yksi_pelaaja(self):
        players = self.stats.team("PIT")
        self.assertEqual(len(players), 1)
        self.assertEqual(players[0].name, "Lemieux")

    def test_team_ei_loydy(self):
        players = self.stats.team("NYR")
        self.assertEqual(len(players), 0)

    def test_top_yksi(self):
        top = self.stats.top(1)
        self.assertEqual(len(top), 1)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[0].points, 124)

    def test_top_kaksi(self):
        top = self.stats.top(2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[0].points, 124)
        self.assertEqual(top[1].name, "Lemieux")
        self.assertEqual(top[1].points, 99)

    def test_top_kaikki(self):
        top = self.stats.top(5)
        self.assertEqual(len(top), 5)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[1].name, "Lemieux")
        self.assertEqual(top[2].name, "Yzerman")
        self.assertEqual(top[3].name, "Kurri")
        self.assertEqual(top[4].name, "Semenko")

    def test_top_enemman_kuin_pelaajia(self):
        top = self.stats.top(10)
        self.assertEqual(len(top), 5)

    def test_top_ilman_parametria_oletusarvo_points(self):
        top = self.stats.top(3)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[0].points, 124)
        self.assertEqual(top[1].name, "Lemieux")
        self.assertEqual(top[1].points, 99)
        self.assertEqual(top[2].name, "Yzerman")
        self.assertEqual(top[2].points, 98)

    def test_top_sort_by_points(self):
        top = self.stats.top(3, SortBy.POINTS)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[0].points, 124)
        self.assertEqual(top[1].name, "Lemieux")
        self.assertEqual(top[1].points, 99)
        self.assertEqual(top[2].name, "Yzerman")
        self.assertEqual(top[2].points, 98)

    def test_top_sort_by_goals(self):
        top = self.stats.top(3, SortBy.GOALS)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Lemieux")
        self.assertEqual(top[0].goals, 45)
        self.assertEqual(top[1].name, "Yzerman")
        self.assertEqual(top[1].goals, 42)
        self.assertEqual(top[2].name, "Kurri")
        self.assertEqual(top[2].goals, 37)

    def test_top_sort_by_assists(self):
        top = self.stats.top(3, SortBy.ASSISTS)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[0].assists, 89)
        self.assertEqual(top[1].name, "Yzerman")
        self.assertEqual(top[1].assists, 56)
        self.assertEqual(top[2].name, "Lemieux")
        self.assertEqual(top[2].assists, 54)

