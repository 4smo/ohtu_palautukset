"""Flask web-sovellus kivi-paperi-sakset pelille."""

from flask import Flask, render_template, request, session, redirect, url_for
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)
app.secret_key = "kivi-paperi-sakset-secret-key"

# Voittojen määrä pelin voittamiseen
VOITTORAJA = 5

# Tallenna tekoälyt sessioiden välillä
tekoalyt = {}


def hae_tekoaly(session_id, pelityyppi):
    """Hakee tai luo tekoälyn sessiolle."""
    key = f"{session_id}_{pelityyppi}"
    if key not in tekoalyt:
        if pelityyppi == "helppo":
            tekoalyt[key] = Tekoaly()
        elif pelityyppi == "vaikea":
            tekoalyt[key] = TekoalyParannettu(10)
    return tekoalyt.get(key)


def poista_tekoaly(session_id, pelityyppi):
    """Poistaa tekoälyn sessiosta."""
    key = f"{session_id}_{pelityyppi}"
    if key in tekoalyt:
        del tekoalyt[key]


@app.route("/")
def etusivu():
    """Näyttää pelin valintasivun."""
    return render_template("etusivu.html")


@app.route("/peli/<pelityyppi>")
def peli(pelityyppi):
    """Näyttää pelisivun."""
    if "peli_id" not in session:
        session["peli_id"] = str(id(session))

    # Alusta uusi peli jos ei ole käynnissä
    if f"{pelityyppi}_ekan_pisteet" not in session:
        session[f"{pelityyppi}_ekan_pisteet"] = 0
        session[f"{pelityyppi}_tokan_pisteet"] = 0
        session[f"{pelityyppi}_tasapelit"] = 0
        session[f"{pelityyppi}_historia"] = []
        session[f"{pelityyppi}_peli_ohi"] = False

    # Tarkista onko peli voitettu
    peli_ohi = session.get(f"{pelityyppi}_peli_ohi", False)
    voittaja = None
    if session[f"{pelityyppi}_ekan_pisteet"] >= VOITTORAJA:
        peli_ohi = True
        voittaja = "Pelaaja 1"
        session[f"{pelityyppi}_peli_ohi"] = True
    elif session[f"{pelityyppi}_tokan_pisteet"] >= VOITTORAJA:
        peli_ohi = True
        if pelityyppi == "kaksinpeli":
            voittaja = "Pelaaja 2"
        else:
            voittaja = "Tietokone"
        session[f"{pelityyppi}_peli_ohi"] = True

    # Hae viimeisin kierros
    historia = session.get(f"{pelityyppi}_historia", [])
    viimeisin_kierros = historia[-1] if historia else None

    return render_template(
        "peli.html",
        pelityyppi=pelityyppi,
        ekan_pisteet=session[f"{pelityyppi}_ekan_pisteet"],
        tokan_pisteet=session[f"{pelityyppi}_tokan_pisteet"],
        tasapelit=session[f"{pelityyppi}_tasapelit"],
        historia=session[f"{pelityyppi}_historia"],
        peli_ohi=peli_ohi,
        voittaja=voittaja,
        voittoraja=VOITTORAJA,
        viimeisin_kierros=viimeisin_kierros,
    )


@app.route("/siirto/<pelityyppi>", methods=["POST"])
def tee_siirto(pelityyppi):
    """Käsittelee pelaajan siirron."""
    if "peli_id" not in session:
        return redirect(url_for("peli", pelityyppi=pelityyppi))

    # Älä salli siirtoja jos peli on ohi
    if session.get(f"{pelityyppi}_peli_ohi", False):
        return redirect(url_for("peli", pelityyppi=pelityyppi))

    ekan_siirto = request.form.get("siirto")

    if ekan_siirto not in ("k", "p", "s"):
        return redirect(url_for("peli", pelityyppi=pelityyppi))

    # Määritä toisen pelaajan/tekoälyn siirto
    if pelityyppi == "kaksinpeli":
        # Kaksinpelissä tallennetaan ensimmäinen siirto ja odotetaan toista
        if "odottava_siirto" not in session:
            session["odottava_siirto"] = ekan_siirto
            return render_template(
                "odota_toista.html",
                pelityyppi=pelityyppi,
                ekan_pisteet=session[f"{pelityyppi}_ekan_pisteet"],
                tokan_pisteet=session[f"{pelityyppi}_tokan_pisteet"],
                tasapelit=session[f"{pelityyppi}_tasapelit"],
            )
        else:
            tokan_siirto = ekan_siirto
            ekan_siirto = session.pop("odottava_siirto")
    else:
        # Tekoälypeli
        tekoaly = hae_tekoaly(session["peli_id"], pelityyppi)
        tokan_siirto = tekoaly.anna_siirto()

        # Parannettu tekoäly oppii pelaajan siirroista
        if pelityyppi == "vaikea":
            tekoaly.aseta_siirto(ekan_siirto)

    # Käytä Tuomari-luokkaa tuloksen määrittämiseen
    tuomari = Tuomari()
    tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)

    # Päivitä pisteet
    session[f"{pelityyppi}_ekan_pisteet"] += tuomari.ekan_pisteet
    session[f"{pelityyppi}_tokan_pisteet"] += tuomari.tokan_pisteet
    session[f"{pelityyppi}_tasapelit"] += tuomari.tasapelit

    # Määritä tulos tekstinä
    siirto_nimet = {"k": "Kivi", "p": "Paperi", "s": "Sakset"}
    if tuomari.ekan_pisteet > 0:
        tulos = "Pelaaja 1 voitti!"
    elif tuomari.tokan_pisteet > 0:
        if pelityyppi == "kaksinpeli":
            tulos = "Pelaaja 2 voitti!"
        else:
            tulos = "Tietokone voitti!"
    else:
        tulos = "Tasapeli!"

    # Lisää historiaan
    historia = session[f"{pelityyppi}_historia"]
    vastustaja = "Pelaaja 2" if pelityyppi == "kaksinpeli" else "Tietokone"
    historia.append(
        {
            "pelaaja1": siirto_nimet[ekan_siirto],
            "vastustaja": siirto_nimet[tokan_siirto],
            "tulos": tulos,
        }
    )
    session[f"{pelityyppi}_historia"] = historia
    session.modified = True

    return redirect(url_for("peli", pelityyppi=pelityyppi))


@app.route("/nollaa/<pelityyppi>")
def nollaa_peli(pelityyppi):
    """Nollaa pelin pisteet."""
    session[f"{pelityyppi}_ekan_pisteet"] = 0
    session[f"{pelityyppi}_tokan_pisteet"] = 0
    session[f"{pelityyppi}_tasapelit"] = 0
    session[f"{pelityyppi}_historia"] = []
    session[f"{pelityyppi}_peli_ohi"] = False

    if "peli_id" in session:
        poista_tekoaly(session["peli_id"], pelityyppi)

    return redirect(url_for("peli", pelityyppi=pelityyppi))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
