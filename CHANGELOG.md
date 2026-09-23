# Breytingaskrá — Brakið (Giskleikur)

Þessi skrá heldur utan um hvað breyttist milli útgáfa. Útgáfunúmerið hér á að
passa við `APP_VERSION` fremst í `brakid` HTML-skránni og við Git-taggið
(`git tag vX.Y.Z`) sem birt var undir.

Snið á hverri færslu:

```
## vX.Y.Z — ÁÁÁÁ-MM-DD
- Hvað breyttist, í stuttu máli, eitt atriði í línu.
```

---

## v1.27.1 — 2026-09-23
- v1.28 reyndist bilað og var lagt til hliðar (ekki notað áfram).
- Byggt ofan á síðustu virku útgáfu (v1.27): sama útgáfumerking og í v1.28
  (`APP_VERSION` / `APP_VERSION_DATE`, útgáfumerki neðst t.v., `console.log`
  við ræsingu) sett inn í `bonusdeild_giskleikur_v1_27_1.html`.
- ATH: kannaðu hvað nákvæmlega var öðruvísi í v1.28 (sem virkaði ekki) svo
  þær breytingar glatist ekki — þessi útgáfa er v1.27 + útgáfumerking, ekkert
  annað úr v1.28 er innifalið.

## v1.28.0 — 2026-09-22 (BILAÐ — ekki í notkun)
- Bætt við útgáfumerkingu: `APP_VERSION` / `APP_VERSION_DATE` fremst í
  skránni, lítið útgáfumerki neðst t.v. í viðmótinu, og `console.log` við
  ræsingu — til að sjá strax hvaða útgáfu notandi er með.
- Þessi CHANGELOG-skrá stofnuð.
- Reyndist bilað í notkun 2026-09-23 — orsök ekki greind hér, sjá v1.27.1.

## Fyrri saga (samantekt, ekki nákvæm útgáfa fyrir útgáfu)
- Náð í fyrra falli (um v1.25): fullur innskráningarferill, hópstjórnun,
  stjórnendaspjald og litastilling liða.
- Á undan því: fjölspilunar-deildarkerfi, viðvarandi auðkenni leikmanna,
  stjórnendaspjald, bónusspár-flipi og hópstjórnun byggð upp í nokkrum
  skrefum.
- Endurskrifað síðar til að vera Supabase-bakað: innskráning með
  tölvupósti/lykilorði, aðgangskóðar, vistun eftir umferðum, "drag-and-drop"
  flipar og litaþema liða.

*(Fylltu inn nákvæmar færslur fyrir v1.26–v1.27 ef þú manst hvað breyttist í
þeim — annars er í lagi að láta samantektina hér að ofan duga sem sögulegan
bakgrunn og byrja nákvæma skráningu núna, frá v1.28.0.)*

---

## Verklag fram á við
1. Þegar breyting er tilbúin til birtingar: hækkaðu `APP_VERSION` (og
   `APP_VERSION_DATE`) efst í HTML-skránni.
2. Bættu við nýrri færslu efst í þessari skrá (fyrir ofan síðustu færslu).
3. Commit-aðu í Git, `git tag vX.Y.Z`, `git push --tags`.
4. Búðu til samsvarandi GitHub Release með sömu punktum og hér.
