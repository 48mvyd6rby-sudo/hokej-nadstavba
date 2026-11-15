# Nadstavba Ligy mladšího dorostu 2026/27

Jednoduchý veřejný web, který automaticky sleduje pořadí v 12 skupinách na stránce Českého hokeje, vybírá první **dva způsobilé** týmy z každé skupiny a zobrazuje 24 postupujících ve 4 *orientačních* geografických skupinách po 6 týmech.

## Publikování zdarma – GitHub Pages (přibližně 5 kroků)

1. Přihlaste se na https://github.com a vytvořte nový **public** repozitář, například `hokej-nadstavba` (bez šablony README).
2. Rozbalte ZIP a nahrajte **obsah** složky `hokej_nadstavba_online` do kořene repozitáře. Je nutné zachovat také skrytou složku `.github/workflows/update.yml` (při nahrávání přes web lze zvolit „Add file → Upload files“ a přetáhnout všechny soubory včetně složky `.github`). Potvrďte „Commit changes“.
3. V **Settings → Pages → Build and deployment** nastavte **Deploy from a branch**, větev `main`, složku `/ (root)` a uložte.
4. V záložce **Actions** otevřete „Aktualizace tabulek Českého hokeje“ a klikněte na **Run workflow**. Případně při prvním spuštění schvalte použití Actions. Pokud commit neprojde kvůli právům, v **Settings → Actions → General → Workflow permissions** nastavte **Read and write permissions**. Veřejný odkaz se následně objeví v **Settings → Pages**.
5. Hotový odkaz bude obvykle `https://UZIVATEL.github.io/hokej-nadstavba/`. Tento odkaz lze libovolně sdílet a po dalších aktualizacích zůstane stejný.

*Naplánované GitHub Actions se mohou spustit se zpožděním; automatická aktualizace není garantována přesně každé dvě hodiny. U veřejných repozitářů GitHub může plánované běhy po delší neaktivitě pozastavit. Stav je vidět v Actions.*

## Co se aktualizuje

- Plán: GitHub Actions spouští `python update.py` každé dvě hodiny (UTC), lze spustit i ručně.
- Zdroj: https://ceskyhokej.cz/competition/standings/85
- Vyhodnocení: 1. a 2. místo z každé základní skupiny podle **oficiálního pořadí**; týmy `EAC Junior Capitals` a `METROPOLIA Silesia` se pro účel postupu přeskočí.
- Rozdělení A–D: *pouze pracovní geografický návrh*, nikoli oficiální los či potvrzené složení skupin. V kódu `update.py` lze později změnit `REGIONS`.
- Po úspěšné kontrole se obnoví `data.json` a s ním veřejná stránka.
- Když kontrola selže, starší ověřený `data.json` zůstává beze změny a běh Action skončí chybou. Datum poslední úspěšné kontroly je veřejně vidět.
- Tlačítko **Zkontrolovat nejnovější data** znovu načte poslední vydaný `data.json`, **nespouští** přímo získávání dat ze zdrojového webu.

## Test a lokální spuštění

```bash
pip install -r requirements.txt
python update.py
python -m http.server 8000
```

Otevřete http://localhost:8000. Aktualizace předpokládá veřejně dostupnou serverem vykreslenou HTML tabulku (nevyužívá neveřejné API). Při změně HTML struktury webu Českého hokeje bude třeba upravit parser.

## Poznámka k datům v ZIP

Přiložená `data.json` je **výchozí snímek** týmů z 15. listopadu 2026. Dokud se úspěšně nespustí první Action, nejde o aktuální stav. Skript v tomto prostředí nebylo možné spustit proti živému webu, protože zde není přímý internetový přístup pro Python; podklady byly ověřeny samostatným čtením veřejného webu.
