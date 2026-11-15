# Grafická aktualizace – ledový design BK Havlíčkův Brod

Tento balíček zachovává původní funkci aktualizace 12 skupin, výběr 24 postupujících, návrh čtyř skupin, úplnou tabulku skupiny 8 a statistiky Petra Pálka. Nově obsahuje ledové pozadí, znak klubu, dodanou fotografii Petra Pálka a vodorovný jednorádkový přehled šesti statistik (na úzkých mobilech se celý pás může horizontálně posunout).

## Nasazení na existující GitHub Pages

1. Otevřete repozitář `48mvyd6rby-sudo/hokej-nadstavba`.
2. Do **kořenové složky repozitáře** nahrajte `index.html`, složku `assets` a ostatní soubory ze ZIP. Při výzvě potvrďte nahrazení stejných souborů.
3. **Zachovejte umístění** `assets/ice-rink.webp`, `assets/bk-havlickuv-brod.png` a `assets/petr-palek.jpg` vedle `index.html`.
4. Po commitu načtěte `https://48mvyd6rby-sudo.github.io/hokej-nadstavba/` (případně s obnovením bez cache).
5. GitHub Actions dále pracuje dle `.github/workflows/update.yml`, aktualizuje `data.json` každé dvě hodiny. Tlačítko obnovit načítá poslední publikovaný `data.json` a samo nespouští nové načtení ze serveru Českého hokeje.

### Důležité

- Údaje zobrazované v tabulkách jsou **živě aktualizované přes datový soubor**, nikoli hodnoty z ilustrativního vizuálního návrhu.
- Skupina, do které právě patří BK Havlíčkův Brod, a řádek klubu se zvýrazňují automaticky. Pokud by klub nepostupoval, v nadstavbových tabulkách zvýraznění nebude; ve skupině 8 zůstane.
- Obrázek hráče je pevně uložen v `assets/petr-palek.jpg`; statistiky se aktualizují z profilu Českého hokeje.
- Logo je použito z veřejného profilu klubu v malé kvalitě. Pro ostré zobrazení ve vysokém rozlišení je vhodné nahradit jej originálním transparentním PNG či SVG se stejným názvem.
- Jde o neoficiální informační projekt a navržené rozdělení skupin není potvrzené Českým hokejem.

---

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

## Aktualizace listopad 2026 – BK Havlíčkův Brod a Petr Pálek

Tato verze navíc barevně zvýrazňuje **nadstavbovou skupinu s BK Havlíčkův Brod** (dynamicky z obsahu dat) a řádek BK Havlíčkův Brod. Pod nadstavbou zobrazuje úplnou **tabulku 1. části, skupiny 8** a **statistiky Petra Pálka** pro Ligu mladšího dorostu 2026/27.

`update.py` načítá ze stejné oficiální stránky úplnou tabulku skupiny 8 včetně jejího záhlaví, dále z `https://ceskyhokej.cz/player/detail/9285` statistiky hráče. Ukládá do `data.json` položky `group8`, `player` a `player_updated_at`. Plán GitHub Actions každé dvě hodiny zůstává beze změny. Pokud se profil hráče nepodaří stáhnout nebo změní strukturu, ostatní tabulky se nadále aktualizují a hráčské statistiky zůstávají na posledních ověřených hodnotách s původním časem aktualizace.

**Nasazení na stávající GitHub Pages:** Rozbalte balíček a nahraďte v kořeni repozitáře `hokej-nadstavba` soubory `index.html`, `update.py`, `data.json` a případně `README.md`. Soubor `.github/workflows/update.yml` se nemění. Potom v záložce **Actions** spusťte workflow **Aktualizace tabulek Českého hokeje** tlačítkem **Run workflow**. Zkontrolujte výsledek běhu a otevřete stále stejnou URL `https://48mvyd6rby-sudo.github.io/hokej-nadstavba/`.

Poznámka: Výchozí tabulka skupiny 8 a statistiky hráče v balíčku odpovídají údajům ověřeným 15. 11. 2026, nejsou zárukou aktuálního stavu. První spuštění `update.py` je znovu aktualizuje.
