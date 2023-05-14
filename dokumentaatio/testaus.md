# Testausdokumentti

Sovellus on testattu sekä unittest moduulin automatisoitujen testien kautta, että tuttujen ja oman toimesta. Testauksen aikana käytän ei pysyvää tietokantayhteyttä(`:memory:`), joten tuotantotiedot olisi eristettyneenä. Molemman {user,dwg}_mgr_test.py

## Yksikkö- ja integraatiotestaus

### Sovelluslogiikka

Tämä oli 1 iso kokonaisuus, nyt on 2 pienempää, joista [UserManager](/src/backend/user_mgmt.py) luokan testejä pystyin hyvinkin pieniksi paloiksi paloitella, kuten kuuluisikin, mutta kun [DrawingManager](/src/backend/dwg_mgmt.py) luokan testit vaativat myös talletusta ja tiukkaa järjestystä testien välissä, joten loppujen lopuksi päätin jättämään se isoksi kokonaisuudeksi (välttän toistuvia testejä).

`DummyCanvas` ja `dummy_callback`:in avulla pystyi hyvin kattavasti luoda käyttöliittymän näkökulmasta testejä. Tämä ei ehkä ole hyvin tehokasta paikata modauksen jälkeen rikkimenneitä kohtia, mutta ainakin kertoo luotettavasti, jos jotain menikin rikki!

### Piirros ja Käyttäjä luokat

Kuten yllä mainitsin, rakensin testit "ylhältä alaspäin" mieluummin kuin alhalta ylöspäin, joten näitä eksplisiittisesti en ole testannut, vaan muutamaa asiaa DrawingManager:in kohdalla Piirrokseen liittyen. 

### Testikattavuus

![](/dokumentaatio/pics/coverage.png)

## Järjestelmäkattavuus

Suoritettu manuaalisesti

### Toiminnallisuudet

[Vaatimusmäärittely](/dokumentaatio/vaatimusmaarittely.md):n mukaisesti kaikki toimii.

## Sovellukseen jääneet laatuongelmat

En ole kerennyt vielä suojata piirroksen pienin ja isoin sallitun koon, esim `miljoona` x `miljoona` iso piirros ois ihan "fine", paitsi käyttökelvotonta!

Myös Canvas:in korkeus muuntaa nappuloiden välissä olevaa rakoa.

Käyttäjälle ei oo kerrottu, vaan oppii kantapään kautta kumpi sarake väri vaikuttaa teksteihin JA viivoihin.
