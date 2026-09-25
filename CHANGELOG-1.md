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

## v1.29.1 — 2026-09-25
- **ALVARLEG LAGFÆRING (mögulegt gagnatap):** fundinn og lagaður galli sem gat
  þurrkað út vistaða giskun leikmanns í hljóði, án nokkurrar villuskilaboða.
- Orsök: `window.storage.get` gaf sömu villu bæði þegar gögn fundust
  einfaldlega ekki enn (fyrsta skráning) OG þegar raunveruleg
  nettengingar-/gagnagrunnsvilla átti sér stað. Allir staðir sem sóttu eigin
  giskun (við ræsingu, við að skipta um hóp, við að ganga í hóp, við að
  breyta nafni) meðhöndluðu þetta tvennt eins og hunsuðu villuna þegjandi og
  hljóðalaust — sem þýddi að ef sóknin klikkaði rétt einu sinni, hélt appið
  að spá viðkomandi væri einfaldlega tóm. Þar sem "Vista allt"-hnappurinn er
  sá sami hvort sem verið er að skrá eigin giskun EÐA (fyrir stjórnendur)
  raunveruleg úrslit leikja, gat næsta smellur á "Vista" — jafnvel þótt hann
  ætti bara að skrá úrslit — skrifað þessa tómu, staðbundnu stöðu yfir
  réttilega vistaða giskun leikmannsins úti í gagnagrunninum.
- Lagað: `window.storage.get` merkir núna skýrt hvort villan þýði „ekkert
  til enn" (öruggt) eða raunveruleg villa (óöruggt). Ef raunveruleg villa
  kemur upp við að sækja eigin giskun er vistun hennar læst (`saveAll`
  hafnar að skrifa yfir hana) þar til síðan er endurhlaðin og sóknin tekst,
  og notandinn fær skýr skilaboð um þetta strax við ræsingu og aftur ef
  reynt er að vista á meðan. Raunveruleg úrslit leikja (stjórnandi) vistast
  áfram eðlilega, óháð þessu.
- ATH til Árna: ef þín eigin giskun fyrir umferð 1 var þurrkuð út með
  þessum hætti, er ekki hægt að endurheimta hana úr appinu sjálfu — hún
  þyrfti að nást úr Supabase-gagnagrunninum (t.d. Point-in-Time Recovery,
  ef virkt), annars þarf að giska aftur (sem er ekki lengur hægt fyrir
  læsta umferð). Láttu mig vita ef þú vilt aðstoð við að athuga hvort
  eldra gildið sé enn til í Supabase.

## v1.29.0 — 2026-09-24
- Ný eiginleiki: hægt að sjá giskanir annarra í hópnum, umferð fyrir umferð.
- Í hverjum umferðarflipa ("Leikir 1–11" o.s.frv.) birtist hnappurinn „Sjá
  giskanir hópsins" um leið og umferðin læsist (60 mín. fyrir fyrsta leik) —
  aldrei fyrr, svo enginn geti afritað spár annarra áður en umferð lokast.
- Við að opna hnappinn sést, fyrir hvern leik í umferðinni, hvaða lið hver
  leikmaður í hópnum valdi (nafn birtist undir liðinu sem viðkomandi
  giskaði á), og hvort það reyndist rétt eða rangt um leið og úrslit eru
  skráð (grænn/rauður litur).
- Notar gögn sem appið sótti nú þegar til að reikna út hópstöðuna í
  „Hópurinn"-flipanum — engin ný fyrirspurn í gagnagrunninn.
- Aðeins sýnilegt þeim sem eru skráðir í hóp (ekki í einkaham).

## v1.28.2 — 2026-09-24
- Lagfært: við ósk um "gleymt lykilorð" fór notandi stundum beint inn í
  appið sjálft í stað þess að sjá skjáinn til að setja nýtt lykilorð —
  gerðist einkum ef notandinn var þegar innskráður í sama vafra.
- Orsök: kapphlaup (race condition) milli tveggja Supabase-atburða —
  `SIGNED_IN` (samstundis, af geymdri innskráningu) og `PASSWORD_RECOVERY`
  (ósamstillt, kemur aðeins seinna). Þegar `SIGNED_IN` var afgreitt á undan
  hélt appið að notandinn ætti bara að fara inn í leikinn, áður en
  `PASSWORD_RECOVERY`-atburðurinn náði að setja rétta stöðu.
- Lagað með því að greina `type=recovery` beint úr vefslóðinni (samstundis,
  strax við ræsingu síðunnar) í stað þess að reiða sig eingöngu á
  ósamstillta Supabase-atburðinn. Þannig veit appið um leið og síðan opnast
  að um lykilorðs-endurheimt sé að ræða, óháð því í hvaða röð Supabase
  atburðirnir berast.
- Eftir að nýtt lykilorð er staðfest er `type=recovery` fjarlægt úr
  vefslóðinni, svo endurhleðsla á síðunni eftir það fari ekki aftur í
  endurheimtar-ham.

## v1.28.1 — 2026-09-24
- Útgáfumerkið var of ósýnilegt (dauft, neðst t.v. yfir alla síðuna) — bætt
  við skýrri, sýnilegri útgáfumerkingu (`v1.28.1`) inni í sjálfum
  hnappa­röðinni (við hliðina á "Skrá út") á aðalskjá leiksins, stíluð eins
  og hinir hnapparnir svo hún týnist ekki.
- Gamla, dauflega merkið neðst t.v. fær að halda sér óbreytt (birtist líka á
  innskráningarskjá), en nýja merkið er það sem sést best í sjálfum leiknum.

## v1.27.1 — 2026-09-23 / uppfært 2026-09-24
- v1.28 reyndist bilað og var lagt til hliðar (ekki notað áfram).
- Byggt ofan á síðustu virku útgáfu (v1.27): sama útgáfumerking og í v1.28
  (`APP_VERSION` / `APP_VERSION_DATE`, útgáfumerki neðst t.v., `console.log`
  við ræsingu) sett inn í `bonusdeild_giskleikur_v1_27_1.html`.
- Borið saman v1.27 og v1.28 í smáatriðum (diff): eini munurinn reyndist
  vera nafnabreytingin úr "Bónusdeild karla / Bónusdeild giskleikur" yfir í
  "Brakið" — hvergi notuð forritunarlega, eingöngu birt sem `<title>` og á
  innskráningarskjá. Engin önnur virkni eða kóði var öðruvísi milli
  útgáfnanna tveggja.
- 2026-09-24: "Brakið"-nafnið því sett aftur inn í v1.27.1 (síðuheiti og
  fyrirsögn á innskráningarskjá), þar sem sú breyting reyndist alveg örugg
  og ótengd því sem klikkaði í v1.28.
- ATH: af því v1.27 og v1.28 voru annars orðrétt eins liggur núverandi
  "bilun" ekki í sjálfum kóðanum í þessari skrá — hún er líklega í hýsingu,
  skyndiminni í vafra, eða Supabase-ástandi frekar en í frumkóðanum sjálfum.

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
