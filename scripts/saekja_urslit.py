# Sækir úrslit og dagskrá Bónusdeildar karla frá korfustatt.is og vistar í urslit.json
# (í rót repo-sins, við hlið index.html). Keyrt af GitHub Action: .github/workflows/urslit.yml
# Byggt á Colab-skriptunni hans Árna; sama þáttun, en skrifar aðeins skrána ef úrslit/dagskrá breytast.

import json
import re
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

SEASON = 2027          # 2027 = tímabilið 2026-27
GENDER = "Ka"          # "Ka" = karlar, "Kv" = konur
URL = f"https://www.korfustatt.is/Timabil/{GENDER}/{SEASON}"
OUT = Path(__file__).resolve().parent.parent / "urslit.json"


def fetch_html(url=URL):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Brakid urslit)"}, timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


def parse(html):
    """Finnur töflurnar eftir dálkaheitum, ekki eftir röð."""
    standings = results = fixtures = None
    for t in pd.read_html(StringIO(html)):
        cols = set(map(str, t.columns))
        if {"Félag", "L", "S", "T"} <= cols:
            standings = t
        elif {"Dagur", "Leikur", "Úrslit"} <= cols:
            results = t
        elif {"Dagur", "Leikur", "Tími"} <= cols:
            fixtures = t
    return standings, results, fixtures


def split_game(text):
    parts = re.split(r"\s+-\s+", str(text).strip(), maxsplit=1)
    return (parts[0].strip(), parts[1].strip()) if len(parts) == 2 else (str(text).strip(), "")


def iso_date(text):
    d, mo, y = str(text).strip().split(".")
    return f"{int(y):04d}-{int(mo):02d}-{int(d):02d}"


def clean_results(df):
    rows = []
    for _, r in df.iterrows():
        m = re.match(r"\s*(\d+)\s*[-:]\s*(\d+)", str(r["Úrslit"]))
        if not m:
            continue  # ekki spilaður / vantar úrslit
        home, away = split_game(r["Leikur"])
        try:
            date = iso_date(r["Dagur"])
        except ValueError:
            date = ""
        rows.append({
            "date": date,
            "venue": str(r.get("Völlur", "") or ""),
            "home": home,
            "away": away,
            "home_score": int(m.group(1)),
            "away_score": int(m.group(2)),
        })
    return rows


def clean_fixtures(df):
    rows = []
    for _, r in df.iterrows():
        home, away = split_game(r["Leikur"])
        try:
            date = iso_date(r["Dagur"])
        except ValueError:
            continue
        rows.append({
            "date": date,
            "time": str(r.get("Tími", "") or ""),
            "venue": str(r.get("Völlur", "") or ""),
            "home": home,
            "away": away,
        })
    return rows


def main():
    _, results, fixtures = parse(fetch_html())
    if results is None:
        sys.exit("Fann ekki úrslitatöfluna á korfustatt.is. Útlit síðunnar gæti hafa breyst.")

    data = {
        "source": URL,
        "results": clean_results(results),
        "fixtures": clean_fixtures(fixtures) if fixtures is not None else [],
    }

    # Skrifa aðeins ef eitthvað breyttist, svo ekki komi commit (og ný Pages-útgáfa) í hverri keyrslu.
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        if old.get("results") == data["results"] and old.get("fixtures") == data["fixtures"]:
            print(f"Engin breyting ({len(data['results'])} úrslit).")
            return

    data["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Vistaði {OUT.name}: {len(data['results'])} úrslit, {len(data['fixtures'])} leikir á dagskrá.")


if __name__ == "__main__":
    main()
