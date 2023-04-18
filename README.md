# Art+ (OhTe assignment)

Sovelluksen avulla surkeimmat käyttäjätkin pystyy luoda mahtavia avantgarde kuvia!

## WiP

hiiren vasemman napin release on valvottu, suorakaiteen, ovalin, viivan laittamiseen tarviit 2 klikkauksen, tekstiä laitetaan yhdellä

## Dokumentaatio
- [vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)
- [työtunnit](dokumentaatio/tunnit.md)
- [muutokset](dokumentaatio/changelog.md)

## Asennus

- Asenna ruuppuvuudet komennolla `poetry install --without dev`
    - Arch Linux:issa asenna myös paketti _tk_ komennolla `sudo pacman -Syy tk`
- Käynnistä sovellus komennolla `poetry run invoke start`

## Muut komentorivitoiminnot

Naihin varmaan tarviit 

- testaaminen `poetry run invoke test` komennolla
- kattavuuden tuonti `poetry run invoke coverage-report` komennolla
    - htmlcov/index.html avattava selaimessa
- linting `poetry run invoke lint` komennolla

