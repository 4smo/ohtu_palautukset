from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


def luo_peli(pelityyppi):
    pelit = {
        "a": KPSPelaajaVsPelaaja,
        "b": KPSTekoaly,
        "c": KPSParempiTekoaly
    }

    peliluokka = pelit.get(pelityyppi)
    
    if peliluokka:
        return peliluokka()
    
    return None
