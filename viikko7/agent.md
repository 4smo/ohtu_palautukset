# Raportti

## Päätyikö agentti toimivaan ratkaisuun?

Kyllä, agentti päätyi toimivaan ratkaisuun. Se rakensi kivi-paperi-sakset -pelille täysin toimivan web-käyttöliittymän Flaskilla.

## Miten varmistuin, että ratkaisu toimii?

Varmistuin ratkaisun toimivuudesta usealla tavalla:
1. Agentti käynnisti sovelluksen ja se lähti pyörimään portissa 5001
2. Testasin sovellusta selaimessa ja pelasin muutaman kierroksen
3. Agentti kirjoitti 19 automatisoitua testiä, jotka kaikki menivät läpi

## Oletko ihan varma, että ratkaisu toimii oikein?

Olen melko varma. Testit kattavat perustoiminnallisuudet, kuten sivujen latautumisen, siirtojen tekemisen, pelin nollauksen ja voittorajan logiikan. Pelasin itse muutaman pelin ja kaikki näytti toimivan. Toki aina voi löytyä reunatapauksia, joita testit eivät kata. Esimerkiksi session käsittelyssä voisi olla ongelmia tuotantoympäristössä.

## Kuinka paljon jouduin antamaan agentille komentoja matkan varrella?

Yllättävän vähän. Annoin käytännössä vain alkuperäisen tehtävänannon.

## Kuinka hyvät agentin tekemät testit olivat?

Testit olivat kohtuullisen kattavat. Ne testasivat:
- Etusivun latautumisen ja sisällön
- Kaikkien pelisivujen latautumisen
- Eri siirtojen (kivi, paperi, sakset) toimivuuden
- Virheellisten siirtojen käsittelyn
- Kaksinpelin vuorojen toiminnan
- Pelin nollauksen

## Onko agentin tekemä koodi ymmärrettävää?

Kyllä, koodi on selkeää:
- Funktiot ja muuttujat on nimetty kuvaavasti suomeksi
- Koodissa on docstringit ja kommentit
- HTML-templateissa on selkeä rakenne ja CSS-tyylit
- Logiikka on jaettu järkevästi eri funktioihin

Erityisen hyvää oli, että agentti käytti olemassa olevia luokkia (`Tuomari`, `Tekoaly`, `TekoalyParannettu`) eikä kirjoittanut niiden logiikkaa uudelleen.

## Miten agentti on muuttanut edellisessä tehtävässä tekemääni koodia?

Agentti ei muuttanut edellisessä tehtävässä refaktoroitua koodia lainkaan. Se:
- Säilytti KiviPaperiSakset-yliluokan ja aliluokat KPSPelaajaVsPelaaja, KPSTekoaly, KPSParempiTekoaly
- Säilytti tehdasfunktion peli_tehdas.py-tiedostossa
- Säilytti alkuperäisen konsolipohjaisen index.py:n

Sen sijaan agentti loi kokonaan uuden app.py-tiedoston web-käyttöliittymää varten ja käytti siinä suoraan Tuomari-, Tekoaly- ja TekoalyParannettu-luokkia. Tämä oli järkevä ratkaisu, koska web-sovelluksen logiikka eroaa merkittävästi konsolisovelluksesta.

## Mitä uutta opin?

Opin useita asioita, kuten session-hallinta flask-sessiossa ja promptien merkityksen.