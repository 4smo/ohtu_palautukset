"""Testit web-sovellukselle."""

import pytest
import sys
import os

# Lisää src-hakemisto polkuun
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, VOITTORAJA


@pytest.fixture
def client():
    """Luo testiasiakkaan."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as client:
        yield client


class TestEtusivu:
    """Testit etusivulle."""

    def test_etusivu_latautuu(self, client):
        """Etusivu latautuu onnistuneesti."""
        response = client.get("/")
        assert response.status_code == 200

    def test_etusivu_sisaltaa_pelityypit(self, client):
        """Etusivu sisältää kaikki pelityypit."""
        response = client.get("/")
        data = response.data.decode("utf-8")
        assert "Kaksinpeli" in data
        assert "Helppo tekoäly" in data or "helppo" in data.lower()
        assert "Vaikea tekoäly" in data or "vaikea" in data.lower()


class TestPeliSivu:
    """Testit pelisivuille."""

    def test_kaksinpeli_sivu_latautuu(self, client):
        """Kaksinpeli-sivu latautuu."""
        response = client.get("/peli/kaksinpeli")
        assert response.status_code == 200

    def test_helppo_tekoaly_sivu_latautuu(self, client):
        """Helppo tekoäly -sivu latautuu."""
        response = client.get("/peli/helppo")
        assert response.status_code == 200

    def test_vaikea_tekoaly_sivu_latautuu(self, client):
        """Vaikea tekoäly -sivu latautuu."""
        response = client.get("/peli/vaikea")
        assert response.status_code == 200

    def test_pelisivu_nayttaa_pisteet(self, client):
        """Pelisivu näyttää pisteet."""
        response = client.get("/peli/helppo")
        data = response.data.decode("utf-8")
        assert "Pelaaja 1" in data


class TestSiirrot:
    """Testit siirroille."""

    def test_kivi_siirto_helppo_tekoaly(self, client):
        """Kivi-siirto helpossa tekoälypelissä toimii."""
        response = client.post(
            "/siirto/helppo", data={"siirto": "k"}, follow_redirects=True
        )
        assert response.status_code == 200

    def test_paperi_siirto_helppo_tekoaly(self, client):
        """Paperi-siirto helpossa tekoälypelissä toimii."""
        response = client.post(
            "/siirto/helppo", data={"siirto": "p"}, follow_redirects=True
        )
        assert response.status_code == 200

    def test_sakset_siirto_helppo_tekoaly(self, client):
        """Sakset-siirto helpossa tekoälypelissä toimii."""
        response = client.post(
            "/siirto/helppo", data={"siirto": "s"}, follow_redirects=True
        )
        assert response.status_code == 200

    def test_virhellinen_siirto_hylätään(self, client):
        """Virheellinen siirto uudellenohjataan pelisivulle."""
        response = client.post(
            "/siirto/helppo", data={"siirto": "x"}, follow_redirects=True
        )
        assert response.status_code == 200

    def test_kaksinpeli_ensimmainen_siirto(self, client):
        """Kaksinpelin ensimmäinen siirto toimii."""
        # Avaa peli ensin
        client.get("/peli/kaksinpeli")
        response = client.post("/siirto/kaksinpeli", data={"siirto": "k"})
        assert response.status_code == 200
        data = response.data.decode("utf-8")
        assert "Pelaaja 2" in data

    def test_kaksinpeli_molemmat_siirrot(self, client):
        """Kaksinpelin molemmat siirrot toimivat."""
        # Ensimmäinen siirto
        client.post("/siirto/kaksinpeli", data={"siirto": "k"})
        # Toinen siirto
        response = client.post(
            "/siirto/kaksinpeli", data={"siirto": "s"}, follow_redirects=True
        )
        assert response.status_code == 200


class TestPelinNollaus:
    """Testit pelin nollaukselle."""

    def test_pelin_nollaus(self, client):
        """Pelin nollaus toimii."""
        # Pelaa ensin
        client.get("/peli/helppo")
        client.post("/siirto/helppo", data={"siirto": "k"}, follow_redirects=True)

        # Nollaa
        response = client.get("/nollaa/helppo", follow_redirects=True)
        assert response.status_code == 200


class TestVaikeaTekoaly:
    """Testit vaikealle tekoälylle."""

    def test_vaikea_tekoaly_toimii(self, client):
        """Vaikea tekoäly pelaa useita kierroksia."""
        client.get("/peli/vaikea")
        for siirto in ["k", "p", "s", "k", "p"]:
            response = client.post(
                "/siirto/vaikea", data={"siirto": siirto}, follow_redirects=True
            )
            assert response.status_code == 200


class TestVoittoraja:
    """Testit voittorajalle (peli päättyy kun joku saa 5 voittoa)."""

    def test_voittoraja_on_oikea(self):
        """Voittoraja on 5."""
        assert VOITTORAJA == 5

    def test_peli_nayttaa_voittorajan(self, client):
        """Pelisivu näyttää voittorajan."""
        response = client.get("/peli/helppo")
        data = response.data.decode("utf-8")
        assert str(VOITTORAJA) in data

    def test_peli_paattyy_kun_voittoraja_saavutetaan(self, client):
        """Peli päättyy kun voittoraja saavutetaan."""
        client.get("/peli/helppo")
        
        # Pelaa kunnes peli päättyy (max 50 kierrosta)
        peli_ohi = False
        for _ in range(50):
            response = client.post(
                "/siirto/helppo", data={"siirto": "k"}, follow_redirects=True
            )
            data = response.data.decode("utf-8")
            if "voitti pelin" in data:
                peli_ohi = True
                break
        
        assert peli_ohi, "Pelin pitäisi päättyä kun voittoraja saavutetaan"

    def test_peli_ei_jatku_voiton_jalkeen(self, client):
        """Siirtoja ei voi tehdä pelin päätyttyä."""
        client.get("/peli/helppo")
        
        # Pelaa kunnes peli päättyy
        for _ in range(50):
            response = client.post(
                "/siirto/helppo", data={"siirto": "k"}, follow_redirects=True
            )
            data = response.data.decode("utf-8")
            if "voitti pelin" in data:
                break
        
        # Yritä tehdä lisäsiirto - pitäisi uudelleenohjata
        response = client.post(
            "/siirto/helppo", data={"siirto": "k"}, follow_redirects=True
        )
        data = response.data.decode("utf-8")
        # Peli on edelleen ohi
        assert "voitti pelin" in data

    def test_uusi_peli_nollaa_voiton(self, client):
        """Uusi peli nollaa voittotilanteen."""
        client.get("/peli/helppo")
        
        # Pelaa kunnes peli päättyy
        for _ in range(50):
            response = client.post(
                "/siirto/helppo", data={"siirto": "k"}, follow_redirects=True
            )
            data = response.data.decode("utf-8")
            if "voitti pelin" in data:
                break
        
        # Nollaa peli
        response = client.get("/nollaa/helppo", follow_redirects=True)
        data = response.data.decode("utf-8")
        
        # Voittobanneri ei näy enää
        assert "voitti pelin" not in data
