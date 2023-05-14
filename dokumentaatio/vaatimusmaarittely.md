# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen avulla surkein käyttäjäkin saa luoda mahtavia avantgarde kuvia.

## Käyttäjät

Alussa tulee olemaan vain _opiskelija_ rooliset käyttäjät, jotkut saavat luoda uusia/avata/tallentaa omia piirroksia. Myöhemmin tehdään _opettaja_ roolin joka pystyy luoda **template** -eja ja avata jokaisen opiskelijan luomat kuvat. **Template** -eja opiskelijatkin saavat avata, jatkaa ja tallentaa omana

## Käyttöliittymäluonnos

Sovelluksessa tulee olemaan alla näkymät:
- [X] login/register/exit
- [X] menu (new/load/exit valinnat)
- [X] piirtonäkymä (save/load/exit napit ainakin tänne)

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista

- [X] Käyttäjä saa luoda järjestelmään käyttäjätunnuksen
  - [X] tunnuksen on oltava ainakin 3 merkkiä ja ainutlaatuinen
- [X] Käyttäjä voi kirjautua järjestelmään
  - [X] Kirjautuminen onnistuu syötettäessä olemassaoleva käyttäjätunnus ja salasana kirjautumislomakkeelle
  - [X] Jos salasana ei täsmää, ilmoittaa järjestelmä tästä

### Kirjautumisen jälkeen

- [X] Käyttäjä saa ladata omat piirokset ja jatkaa ne
- [X] Käyttäjä voi luoda uuden piirroksen
  - [X] opiskelijoiden luomat piirrokset näkyvät ainoastaan sen luoneelle käyttäjälle + opettajille
- [X] Käyttäjä saa lisätä yleisiä elementtejä piirrokselleen
- [X] Käyttäjä saa tallentaa piirroksensa ja nimettää sitä
- [X] Käyttäjä saa ladata omat piirrokset ja **template** -it
- [X] Käyttäjä saa kirjautua ulos

## Jatkokehitysideoita

Muutamaa kehitettävää mitkä varmasti eivät mahdu perustoiminnallisuuteen

- [ ] erillinen register näkymä, alussa meen vaan user:pass siinä login näkymässä..
  - [X] osin toteutettu pop-up ikkunalla
- [ ] drag n drop toiminta eri SVG feature -eille
  - [ ] esim neliö/ympyrä raahattava hiirellä
- [ ] template:in toteutus
- [ ] mahdollisesti *opettajarooli*
- [X] salasanojen monimutkaisuus \w{8,16}
- [ ] piirroksia saa tallentaa tiedostona
- [ ] elementtien järjestys on vaihdettavissa
- [ ] elementtien (rajoitetun määrän) ominaisuudet ovat saadettavissa
- [ ] _Opettaja_ rooliset käyttäjät saa myös avata muiden luomat piirrokset
- [ ] _opettajat_ saavat tallentaa myös **template** -ina
- [X] undo/redo toiminta
- [ ] fontin koon ja tyypin säätö käyttäjän toimesta
- [ ] free line toiminta
