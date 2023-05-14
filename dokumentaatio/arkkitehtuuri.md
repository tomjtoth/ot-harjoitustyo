# Arkkitehtuurikuvaus

## Pakkausrakenne

```mermaid
classDiagram
    Ui ..> Backend
    Backend ..> Entities
```

Pakkaus `Ui` vastaa käyttäjän ja sovelluslogiikan vuorovaikutuksesta. `Backend` kuvaa sovelluslogiikkaa, on vastuullinen eri pakkauksien yhteistyöstä, sekä pysyväistalletuksesta. `Entities` sisältää käyttäjien ja piirrosten luokkia.

## Käyttöliittymä

On 3 päänäkymää, ja 3 ponnahdusikkuna:
- [Kirjautumisnäkymä](/src/ui/login_view.py)
    - Uuden käyttäjän rekisteröinnissä pyydetään salasanaa uudelleen
- [Menu näkymä](/src/ui/menu_view.py)
    - Uuden piirroksen tietojen näkymä
- [Piirtonäkymä](/src/ui/drawing_view.py)
    - Tekstin syöttöikkuna

Näissä 3 päänäkymässä on yhteiset piirteet joita siirsin [View](/src/ui/common.py) luokkaan. Ne myös käyttävät saman ikkunan, joten kerralla vain 1 voi olla aktiivinen ja `Ui` luokka on vastuussa niitten vaihdosta. 

Login näkymä on yksinkertaistettu, ei ole erillistä näkymää rekisteröintiä varten, vaan uusia käyttäjiä luodaan suoraan annetulla `username`:`password` kombolla vahvistuksen jälkeen.

Menu näkymässä käyttäjä saa valita omista piirroksistaan tai luoda uutta, jonka tapauksessa näkymä heittää ponnahdusikkunan johon syötetään uusien piirrosten nimi, leveys ja korkeus.

Piirtonäkymässä yritin matkia kunnon vanha `MS Pain`t; käyttäjä voi säätää laukevien komentojen välillä:

- suorakaide
- oval
- viiva
- teksti

## Sovelluslogiikka

Sovelluksessa 1 [Käyttäjä](/src/entities/user.py) saa omistaa monta [Piirrosta](/src/entities/drawing.py):

```mermaid
classDiagram
    User "1" --> "*" Drawing


class User {
    +Int id
    +String name
    +Boolean teacher
}

class Drawing {
    +String name
    +Int width
    +Int height
    +Int id
    #List content
    #List undo_stack

    +add(cmd, *args, **kwargs)
    +reproduce()
    +stringify()
    +undo()
    +clear_undo_stack()
    +redo()

}
```

Yritin eristää [DrawingManager](/src/backend/dwg_mgmt.py) luokkaan sovelluksen niitä toimintoja jotkut vaikuttaa piirroksiin, myös [UserManager](/src/backend/user_mgmt.py) luokkaan ne toiminnot, jotkut liittyvät tiukasti autentikaatioon. Molemmat moduulit exportoivat 1-1 oliota itsestään, jotkut hoitavat:
- kirjautumisen/rekisteröinnin
- kuvan tallentamisen, listaamisen, modaamisen

```mermaid
classDiagram
    UserManager "1" --> "0-1" User
    DrawingManager "1" --> "0-1" Drawing
    User "1" --> "*" Drawing
```

## Pysyväistalletus

Taustalla SQLite3 hoitaa pysyväistalletusta [conn](/src/backend/database.py) olion kautta, kannassa 4 taulua:

- users
- drawings

- teachers
- templates

2 jälkimmäistä on jatkokehitystä miettien jo luotu valmiiksi. `CREATE TABLE IF NOT EXISTS` lauseiden ansiosta tietokantaa ei tarvitse erikseen rakentaa/alustaa. Python:in kokonaisluvut tallennan `INTEGER`, Stringit `TEXT` muodossa. 
Resurssieni rajoitteista päädyin tallentaa piirrosten sisällön varsin epätehokkaasti, JSON muodossa `TEXT`:ina. SQLite kuitenkin tukee myös JSON scalar funktioita, joten on myös mahdollista laajentaa sovellusta tässä muodossakin!
Tarkemmat tiedot löytyvät yllä moduulin `executescript` kutsusta.

### Tiedosto sijainti

Tietokantaa perustetaan juurihakemiston `backend.db` tiedostoon.

## Päätoiminnallisuudet

### Yhdistetty login/register toiminta

Jos käyttäjä ei ole olemassa, sitä rekisteröidään, pääsy seuraavaan näkymään tapahtuu heti.

```mermaid
---
title: Moitteeton rekisteröintiprosessi
---
sequenceDiagram
    actor User
    
    User->>+UI: click "Login/Register" button
    UI->>+UserManager: login_register("matti", "p4ssW0rD")
    UserManager->>+SQLite: select ... where username == 'matti'
    SQLite-->>-UserManager: 0 rows
    UserManager->>+User: prompt password again
    User-->>UserManager: password matches
    UserManager->>+SQLite: insert into users...;
    SQLite-->>-UserManager: last_row_id
    UserManager->>UserManager: self._curr_user = User(...)
    UserManager-->>-UI: 
    UI->>UI: change to MenuView
    UI-->>-User: 

```

Alla kaaviossa yksi esimerkki miten `UserManager` estää pääsyn ilman oikeeta salasanaa. Tosiaan `WrongPassword` poikkeausta heitetään myös kun rekisteöinnissä pyydetään vahvistamaan käyttäjän sen salasanan, eikä se täsmää ekaa syötettä.

```mermaid
---
title: Väärä salasana sisäänkirjautuen
---
sequenceDiagram
    actor User
    
    User->>+UI: click "Login/Register" button
    UI->>+UserManager: login_register("matti", "lalalalalalala")
    UserManager->>+SQLite: select password, ... where username == 'matti'
    SQLite-->>-UserManager: 1 row
    UserManager->>UserManager: compare 2 passwords
    UserManager-->>-UI: raise WrongPassword
    UI-->>-User: 
```

### Piirrosten valinta ja lataus

Menu näkymän tarkoitus on listata käyttäjän luomat piirrokset, uuden piirroksen luomisen mahdollistaminen, myös nappien avulla luoda yksiselittäistä tapaa päästä näkymien välissä eteenpäin (piirtämään) ja taksepääin (kirjautumalla ulos).

```mermaid
---
title: Vaihto Menu näkymään ja uuden piirroksen luonti
---
sequenceDiagram
    actor User

    UserManager-->>+UI: login/register succeeded
    UI->>UI: change to MenuView
    UI->>+UserManager: get_curr_user()
    UserManager-->>UI: instance of User
    UI->>+DrawingManager: get_user_dwgs(user.id)
    DrawingManager->>+SQLite: query
    SQLite-->>-DrawingManager: possible rows
    DrawingManager-->>-UI: [ possible Drawing instances ]
    UI->>UI: populate listbox, finish creating view
    UI-->>-User: wait for input

    User->>+UI: <NEW DRAWING>
    UI->>+User: prompt title, width, height
    User-->>-UI: str, int, int
    UI->>DrawingManager: set_curr_dwg(Drawing(name, width, height))
    UI->>UI: change to DrawingView
    UI->>UI: populate GUI controls, change TITLE of root window
    UI->>DrawingManager: set default cmd, fill, border
    UI->>DrawingManager: set_canvas(instance of Canvas)
    UI->>DrawingManager: set_text_prompter(UI's public callback)


    UI-->>-User: wait for input
```

Yllä esitetty miten luodaan uuden piirroksen ja siirrytään piirtonäkymään kun piirros on tyhjä. Alla jatketaan siitä kohtaa, että kutsutaan `dwg_mgr.set_curr_dwg( ... )` ja käydään läpi miten olemassa olevat piirteet päätyvät täsmälleen samalla tavalla `tkinter.Canvas`:iin, kuten piirtämisen hetkellä ne olivat.

```mermaid
---
title: Olemassa olevan piirroksen lataus
---
sequenceDiagram
    actor User

    User->>+UI: load existing dwg
    UI->>DrawingManager: set_curr_dwg(instance of Drawing)
    UI->>UI: change to DrawingView
    UI->>UI: populate GUI controls, change TITLE of root window
    UI->>DrawingManager: set default cmd, fill, border
    UI->>+DrawingManager: set_canvas(instance of Canvas)
    DrawingManager->>+Drawing: reproduce()
    Drawing-->>-DrawingManager: generator of (cmd, *args, **kwargs)
    DrawingManager->>+UI: populate Canvas with features
    UI-->>-DrawingManager: tkinter object references
    DrawingManager->>DrawingManager: store references in canv_hist

    DrawingManager-->>-UI: 

    UI->>DrawingManager: set_text_prompter(UI's public callback)



    UI-->>-User: wait for input
```

### Piirteiden lisääminen piirroksiin

Yllä saatiin `Drawing.reproduce()` kutsuen 1 piirre kerralla, joita luotiin Canvas:iin uudelleen kuvan ladattaessa. Tässä seuraavassa kaaviossa lisätään pari piirrettä:
```mermaid
---
title: Oletuspiirteen lisäy piirrokseen
---
sequenceDiagram
    actor User

    User->>+UI: left button pressed on Canvas

    UI->>UI: tkinter Event generated
    UI->>+DrawingManager: b1_dn(event)
    DrawingManager->>DrawingManager: save start coords
    DrawingManager-->>-UI: 
    UI-->>-User: wait for next event


    User->>+UI: drags mouse cursor

    UI->>UI: tkinter Event generated
    UI->>+DrawingManager: b1_mv(event)
    DrawingManager->>+UI: draw feature with current (cmd, fill, border) to event.pos
    UI-->>-DrawingManager: tkinter object ID
    DrawingManager->>DrawingManager: store it in self._preview
    DrawingManager-->>-UI: 
    UI-->>-User: wait for next event

    User->>+UI: drags mouse cursor

    UI->>UI: tkinter Event generated
    UI->>+DrawingManager: b1_mv(event)
    DrawingManager->>UI: delete previous preview by ID
    DrawingManager->>+UI: draw feature with current (cmd, fill, border) to event.pos
    UI-->>-DrawingManager: tkinter object ID
    DrawingManager->>DrawingManager: store it in self._preview
    DrawingManager-->>-UI: 
    UI-->>-User: wait for next event

    User->>+UI: releases left button

    DrawingManager->>UI: delete previous preview by ID
    DrawingManager->>+UI: draw feature with current (cmd, fill, border) to event.pos
    UI-->>-DrawingManager: tkinter object ID
    DrawingManager->>DrawingManager: append it to self._canv_hist
    DrawingManager->>DrawingManager: clear start coords and self._preview
    DrawingManager->>+Drawing: add(cmd, fill, border, *args, **kwargs)
    Drawing->>Drawing: append (cmd, args, kwargs) to content as tuple
    Drawing-->>-DrawingManager: 
    DrawingManager-->>UI: 
    UI-->>-User: wait for next event

```

Tässä vaiheessa käyttäjä on lisännyt ruutuun pienehkon (meillä oli vain 2 hiiren-raahaus tapahtumaa) __suorakaiteen__,  __punaisella__ reunalla ja __vihreällä__ täytteellä (oletuksean). Aktiivinen `Piirros` olio myös laittoi `b1_up` tapahtuman yhteydessä talteen oleelliset tiedot pirteestä. __Viivan__ lisääminen poikkeaa sen verran yllä kuvatulta, että sillä ei ole määritelty väri reunalle, joten tuo puuttuu `kwargs`:sta. __Tekstin__ lisääminen poikkeaa yhä enemmän lopulta 3 piirteeltä alla tavalla:

```mermaid
---
title: Tekstin lisääminen
---
sequenceDiagram
    actor User

    User->>+UI: left button pressed on Canvas
    UI->>+UI: tkinter Event generated
    UI->>DrawingManager: b1_dn(event)
    UI-->>-User: wait for input

    User->>+UI: drags mouse on Canvas
    UI->>+UI: tkinter Event generated
    UI->>DrawingManager: b1_mv(event)
    UI-->>-User: wait for input

    User->>+UI: left button released on Canvas
    UI->>+UI: tkinter Event generated
    UI->>+DrawingManager: b1_up(event)
    DrawingManager->>+UI: call public text_prompter method
    UI->>+User: prompt text
    User-->>-UI: "jotain syöte"
    UI-->>-DrawingManager: str
    DrawingManager->>+UI: create_text(...)
    UI-->>-DrawingManager: tkinter object ID
    DrawingManager->>DrawingManager: append it to self._canv_hist
    DrawingManager->>Drawing: add(cmd, *args, **kwargs)
    DrawingManager-->>-UI: 
    UI-->>-User: wait for input

```

Tekstin lisääminen oli hankalin, koska `DrawingManager`:in piti pystyä pyytää syötteen käyttäjältä siten, että *codebase* olisi edelleen eristettynä

### Piirteiden/värien valinta

Alla kuvatulla tavalla käyttäjä pääsee valitsemaan missä vaiheessa tahansa tulevien piirteiden lajin __ovaaliksi__, jolla __keltainen__ reuna ja __sininen__ täyte.

```mermaid
---
title: Piirteiden ja värien valinta
---
sequenceDiagram
    actor User

    User->>+UI: clicks OVAL radiobutton
    UI->>DrawingManager: set_cmd(OVAL)
    UI-->>-User: wait for input

    User->>+UI: clicks left yellow button
    UI->>DrawingManager: set_border("yellow")
    UI-->>-User: wait for input

    User->>+UI: clicks right blue button
    UI->>DrawingManager: set_fill("blue")
    UI-->>-User: wait for input

```


### Un-/redo toiminta

Käyttäjällä on mahdollisuus perua ja palauttaa peruutut pirteet piirrokseen. Alla tapauksessa oletetaan, että piirrokseen on lisätty tasan 2 piirrettä.

```mermaid
---
title: Piirteiden peruminen
---
sequenceDiagram
    actor User

    User->>+UI: "undo" pressed 1st time

    UI->>+DrawingManager: undo()
    DrawingManager->>+Drawing: undo()
    Drawing->>Drawing: pop last feature from self._content
    Drawing->>Drawing: append it to self._undo.stack
    Drawing->>Drawing: 1 more still in contents
    Drawing-->>-DrawingManager: return True
    DrawingManager->>DrawingManager: pop last ID from self._canv_hist
    DrawingManager->>UI: delete feature from Canvas by ID
    DrawingManager-->>-UI: return True
    UI->>UI: set undo/redo button states accordingly
    UI-->>-User: wait for input

    User->>+UI: "undo" pressed 2nd time

    UI->>+DrawingManager: undo()
    DrawingManager->>+Drawing: undo()
    Drawing->>Drawing: pop last feature from self._content
    Drawing->>Drawing: append it to self._undo.stack
    Drawing->>Drawing: no more features in contents
    Drawing-->>-DrawingManager: return False
    DrawingManager->>DrawingManager: pop last ID from self._canv_hist
    DrawingManager->>UI: delete feature from Canvas by ID
    DrawingManager-->>-UI: return False
    UI->>UI: set undo/redo button states accordingly
    UI-->>-User: wait for input

    User->>+UI: "undo" pressed 3rd time

    UI->>+DrawingManager: undo()
    DrawingManager->>+Drawing: undo()
    Drawing->>Drawing: self._content is empty
    Drawing-->>-DrawingManager: raise EmptyStack
    DrawingManager-->>-UI: return False
    UI->>UI: set undo/redo button states accordingly
    UI-->>-User: wait for input

```

`Redo` toimii samalla periaatella, paitsi se `Drawing.redo()` palauttaa boolean arvon lisäksi palautettavaa piirettäkin, jotta DrawingManager pystyisi sitä lisätä uudelleen Canvas:iin.

```mermaid
---
title: Peruttujen piirteiden palautus
---
sequenceDiagram
    actor User

    User->>+UI: "redo" pressed

    UI->>+DrawingManager: redo()
    DrawingManager->>+Drawing: redo()
    Drawing->>Drawing: pop last feature from self._undo_stack
    Drawing->>Drawing: append it to self._content
    Drawing->>Drawing: more than 1 feature still in undo_stack
    Drawing-->>-DrawingManager: return (True, feature)
    DrawingManager->>+UI: create feature (cmd, *args, **kwargs)
    UI-->>-DrawingManager: tkinter object ID
    DrawingManager->>DrawingManager: self._canv_hist.append(ID)
    DrawingManager-->>-UI: return True
    UI->>UI: set undo/redo button states accordingly
    UI-->>-User: wait for input

```

### Piirroksen tallentaminen

Loppujen lopuksi käyttäjä tallentaa piiroksensa, joka on joko ollut jo olemassa, tai on vasta luotu. Alla kaaviossa katsotaan uudne teoksen talletusta, tosiaan ero suurimmiltaan on `INSERT` vs `UPDATE` lause tietokantaan.
```mermaid
---
title: Uuden piirroksen tallentaminen
---
sequenceDiagram
    actor User

    User->>+UI: "Save and Exit" pressed
    UI->>UI: reset root window's TITLE
    UI->>+DrawingManager: 
    DrawingManager->>+Drawing: stringify()
    Drawing-->>-DrawingManager: self._content as JSON
    DrawingManager->>SQLite: INSERT int drawings ...
    DrawingManager-->>-UI: 
    UI->>UI: change to Menu view

    UI-->>-User: wait for input

```
