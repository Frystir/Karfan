# Ákveður hvort GitHub Action eigi að sækja korfustatt.is í þessari keyrslu.
# Aðeins Python-staðalsafn, svo þetta keyrir áður en pandas o.fl. er sett upp (sparar tíma í "tómum" keyrslum).
#
# Reglur:
#  - Handvirk keyrsla ("Run workflow") eða dagskrárathugun (á 3 klst. fresti): sækja alltaf,
#    svo breyttir leiktímar og síðbúin úrslit skili sér.
#  - Tíðu keyrslurnar á leikjakvöldum (á 10 mín. fresti): sækja aðeins ef leikur er á dagskrá í dag
#    sem hófst fyrir a.m.k. 75 mín. og er ekki enn kominn með úrslit. Ísland er á UTC allt árið.

import json
import os
from datetime import datetime, timezone
from pathlib import Path

DAGSKRAR_CRON = "17 */3 * * *"   # verður að passa við cron-línuna í urslit.yml
MIN_EFTIR_UPPHAF = 75

ROOT = Path(__file__).resolve().parent.parent


def ákvörðun():
    if os.environ.get("EVENT") != "schedule":
        return True, "handvirk keyrsla"
    if os.environ.get("CRON") == DAGSKRAR_CRON:
        return True, "regluleg dagskrárathugun"
    try:
        data = json.loads((ROOT / "urslit.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return True, "urslit.json vantar eða er ólæsileg"

    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    for f in data.get("fixtures", []):
        if f.get("date") != today:
            continue
        try:
            hh, mm = (int(x) for x in str(f.get("time", "")).split(":"))
        except ValueError:
            return True, f"leikur í dag án tíma: {f.get('home')} - {f.get('away')}"
        start_min = hh * 60 + mm
        if now.hour * 60 + now.minute >= start_min + MIN_EFTIR_UPPHAF:
            return True, f"beðið eftir úrslitum: {f.get('home')} - {f.get('away')} ({f.get('time')})"
    return False, "enginn leikur í dag sem bíður úrslita"


if __name__ == "__main__":
    run, why = ákvörðun()
    print(("Sæki: " if run else "Sleppi: ") + why)
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
        fh.write(f"run={'true' if run else 'false'}\n")
