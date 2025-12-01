# Raportti

## Copilotin huomiot koodista

Copilot teki pull requestin katselmoinnissa seuraavat huomiot:

**Pull request overview:**
> This PR refactors the TennisGame class to improve code quality and maintainability by replacing magic numbers with named constants, improving variable naming, and extracting the monolithic get_score method into smaller, well-named helper methods. The refactoring preserves all existing functionality while making the code significantly more readable.

**Key Changes (Copilotin tunnistamat muutokset):**
- Introduced constants `SCORE_NAMES` and `POINTS_TO_WIN` to eliminate magic numbers
- Renamed `m_score1`/`m_score2` to more descriptive `player1_score`/`player2_score`
- Decomposed the complex `get_score` method into six focused helper methods with clear responsibilities

Copilot tunnisti siis kaikki keskeiset parannukset:
1. Taikanumeroiden korvaamisen nimetyillä vakioilla
2. Muuttujien uudelleennimeämisen kuvaavammiksi
3. Ison metodin pilkkomisen pienempiin, selkeästi nimettyihin apumetodeihin

## Ehdottiko Copilot muutoksia?

Ei. Copilot totesi:

> "Perfect! I've completed my thorough review of the code. I found no issues to report. The refactoring is well-done, maintains all the original functionality, and significantly improves code readability and maintainability."

Koska refaktoroitu koodi oli laadukasta, Copilot ei löytänyt parannettavaa eikä ehdottanut muutoksia.

## Kuinka hyödylliseksi koin Copilotin tekemän katselmoinnin?

Copilotin katselmointi ei ollut erityisen hyödyllinen tässä tapauksessa, koska koodi oli jo laadukasta eikä muutosehdotuksia tullut, mutta Copilot tarkisti tennispelilogiikan toimivuuden ja varmisti, että refaktorointi ei rikkonut mitään ja sain vahvistuksen, että tehdyt muutokset olivat oikeansuuntaisia. Koin myös hyödylliseksi, että Copilot tunnisti ja dokumentoi kaikki tehdyt parannukset selkeästi.