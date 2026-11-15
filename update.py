#!/usr/bin/env python3
"""Stáhne aktuální pořadí z ceskyhokej.cz a bezpečně přepíše data.json."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

URL = 'https://ceskyhokej.cz/competition/standings/85'
TARGET = Path(__file__).resolve().parent / 'data.json'
EXCLUDED = ('eac junior capitals', 'metropolia silesia')
# POUZE ORIENTAČNÍ územní návrh (nikoli oficiální rozdělení Českého hokeje).
REGIONS = {
    'A': {'label': 'Západ a Praha', 'groups': [1, 2, 4]},
    'B': {'label': 'Jih a střed', 'groups': [3, 5, 9]},
    'C': {'label': 'Sever a východ Čech', 'groups': [6, 7, 8]},
    'D': {'label': 'Morava a Slezsko', 'groups': [10, 11, 12]},
}
PATTERN = re.compile(r'Liga\s+mladšího\s+dorostu\s+2026\s*/\s*27\s+sk\.?\s*(\d{1,2})\b', re.I)


def norm(s):
    return ' '.join(s.lower().split())


def extract(html):
    soup = BeautifulSoup(html, 'html.parser')
    groups = {}
    # Nadpisy jsou umístěny bezprostředně před tabulkami; nepřidělujeme tabulky
    # podle pevného pořadí v HTML, protože skupina 10 bývá před skupinou 2.
    for heading in soup.find_all(re.compile('^h[1-6]$')):
        match = PATTERN.search(heading.get_text(' ', strip=True))
        if not match:
            continue
        number = int(match.group(1))
        if number in groups or not 1 <= number <= 12:
            raise ValueError(f'Duplicitní nebo neplatná skupina: {number}')
        table = heading.find_next('table')
        next_heading = heading.find_next(re.compile('^h[1-6]$'))
        if table is None or (next_heading is not None and next_heading.sourceline and table.sourceline and next_heading.sourceline < table.sourceline):
            raise ValueError(f'Chybí tabulka pro skupinu {number}')
        rows = []
        for tr in table.find_all('tr'):
            cols = tr.find_all('td', recursive=False)
            if len(cols) < 4:
                continue
            rank_s = cols[0].get_text(' ', strip=True)
            if not re.fullmatch(r'\d+\s*\.?', rank_s):
                continue
            rank = int(re.search(r'\d+', rank_s).group())
            team = cols[1].get_text(' ', strip=True)
            if not team:
                raise ValueError('Prázdné jméno týmu')
            try:
                games = int(cols[2].get_text(' ', strip=True))
                points = int(cols[-1].get_text(' ', strip=True))
            except ValueError as exc:
                raise ValueError(f'Chybná čísla pro {team}') from exc
            link = cols[1].find('a', href=True)
            href = link.get('href', '') if link else ''
            if href.startswith('/'):
                href = 'https://ceskyhokej.cz' + href
            elif not href.startswith('https://ceskyhokej.cz/'):
                href = ''
            rows.append({'name': team, 'original_rank': rank, 'games': games, 'points': points, 'url': href})
        if len(rows) < 3 or len(set(r['name'] for r in rows)) != len(rows):
            raise ValueError(f'Nedostatečná nebo duplicitní data pro skupinu {number}')
        if any(rows[i]['original_rank'] >= rows[i+1]['original_rank'] for i in range(len(rows)-1)):
            raise ValueError(f'Chybná posloupnost pořadí skupiny {number}')
        groups[number] = rows
    if set(groups) != set(range(1, 13)):
        raise ValueError(f'Nenalezeno všech 12 skupin, dostupné: {sorted(groups)}')

    selected = {}
    for number, rows in groups.items():
        eligible = [dict(r, source_group=number) for r in rows if not any(x in norm(r['name']) for x in EXCLUDED)]
        if len(eligible) < 2:
            raise ValueError(f'V {number}. skupině nejsou dva způsobilé týmy')
        selected[number] = eligible[:2]
    regions = []
    for key, settings in REGIONS.items():
        regions.append({'id': key, 'label': settings['label'], 'source_groups': settings['groups'],
                        'teams': [team for g in settings['groups'] for team in selected[g]]})
    if len(regions) != 4 or any(len(r['teams']) != 6 for r in regions):
        raise ValueError('Chybný počet postupujících')
    return {'source': URL, 'rules': 'https://ceskyhokej.cz/competition/description/85',
            'updated_at': datetime.now(ZoneInfo('Europe/Prague')).isoformat(timespec='seconds'),
            'season': '2026/27', 'provisional_regions': True, 'regions': regions,
            'groups': [{'id': n, 'teams': selected[n]} for n in range(1,13)]}


def main():
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0 (compatible; HockeyStandingsTracker/1.0; contact: GitHub Pages project)'}, timeout=40)
    response.raise_for_status()
    response.encoding = response.apparent_encoding if response.encoding is None else response.encoding
    output = extract(response.text)
    temp = TARGET.with_suffix('.json.tmp')
    temp.write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temp.replace(TARGET)
    print(f"OK: {output['updated_at']}, {sum(len(x['teams']) for x in output['regions'])} týmů")


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {exc}; poslední data.json zůstává nezměněn.', file=sys.stderr)
        sys.exit(1)
