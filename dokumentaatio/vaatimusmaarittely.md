# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen avulla surkein käyttäjäkin saa luoda mahtavia avantgarde kuvia.

## Käyttäjät

Alussa tulee olemaan vain _opiskelija_ rooliset käyttäjät, jotkut saavat luoda uusia/avata/tallentaa omia piirroksia. Myöhemmin tehdään _opettaja_ roolin joka pystyy luoda **template** -eja ja avata jokaisen opiskelijan luomat kuvat. **Template** -eja opiskelijatkin saavat avata, jatkaa ja tallentaa omana

## Käyttöliittymäluonnos

Sovelluksessa tulee olemaan alla näkymät:
- login/register/exit
- menu (new/load/exit valinnat)
_ piirtonäkymä (save/load/exit napit ainakin tänne)
  - _opettajat_ saavat tallentaa myös **template** -ina

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista

- Käyttäjä saa luoda järjestelmään käyttäjätunnuksen
  - tunnuksen on oltava ainakin 3 merkkiä ja ainutlaatuinen
- Käyttäjä voi kirjautua järjestelmään
  - Kirjautuminen onnistuu syötettäessä olemassaoleva käyttäjätunnus ja salasana kirjautumislomakkeelle
  - Jos käyttäjää ei olemassa, tai salasana ei täsmää, ilmoittaa järjestelmä tästä

### Kirjautumisen jälkeen

- Käyttäjä saa ladata omat piirokset ja jatkaa ne
- Käyttäjä voi luoda uuden piirroksen
  - opiskelijoiden luomat piirrokset näkyvät ainoastaan sen luoneelle käyttäjälle + opettajille
- Käyttäjä saa lisätä yleisiä SVG elementtejä piirrokselleen
  - elementtien järjestys on vaihdettavissa
  - elementtien (rajoitetun määrän) ominaisuudet ovat saadettavissa
- Käyttäjä saa tallentaa piirroksensa ja nimettää sitä
- Käyttäjä saa ladata omat piirrokset ja **template** -it
  - _Opettaja_ rooliset käyttäjät saa myös avata muiden luomat piirrokset
- Käyttäjä saa kirjautua ulos

## Jatkokehitysideoita

Muutamaa kehitettävää mitkä varmasti eivät mahdu perustoiminnallisuuteen

- erillinen register näkymä, alussa meen vaan user:pass siinä login näkymässä..
- drag n drop toiminta eri SVG feature -eille
  - esim neliö/ympyrä raahattava hiirellä
- template:in toteutus
- mahdollisesti *opettajarooli*