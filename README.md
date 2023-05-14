# Art +

Sovelluksen avulla surkeimmat käyttäjätkin pystyy luoda mahtavia avantgarde kuvia!


## Kuvaus

Tämä on Helsingin Yliopiston eräälle kursille tarkoitettu palautettava tehtävä.


## Dokumentaatio

- [vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)
- [testausdokumentti](dokumentaatio/testaus.md)
- [työtunnit](dokumentaatio/tunnit.md)
- [julkaisut](https://github.com/tomjtoth/ot-harjoitustyo/releases)
- [CHANGELOG](dokumentaatio/changelog.md)


## Asennus

- Asenna ruuppuvuudet komennolla `poetry install --without dev`
    - Arch Linux:issa asenna myös paketti _tk_ komennolla `sudo pacman -Syy tk`
- Käynnistä sovellus komennolla `poetry run invoke start`


## Muut komentorivitoiminnot

Näihin tarvitset loputkin riippuvuuksista, joten aja `poetry install` uudelleen ilman lisälippua.

- testaaminen `poetry run invoke test` komennolla
- kattavuuden tuonti `poetry run invoke coverage-report` komennolla
    - `/htmlcov/index.html` avattava selaimessa` Win32` ympäristössä käsin
- linting `poetry run invoke lint` komennolla
- formatting `poetry run invok format` komennolla
