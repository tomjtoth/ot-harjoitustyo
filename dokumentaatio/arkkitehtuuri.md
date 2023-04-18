# Arkkitehtuurikuvaus

## Pakkausrakenne

```mermaid
classDiagram
    Ui ..> Backend
    Backend ..> Entities
```

Pakkaus `Ui` vastaa käyttäjän ja sovelluslogiikan vuorovaikutuksesta. `Backend` kuvaa sovelluslogiikkaa, on vastuullinen eri pakkauksien yhteistyöstä, sekä pysyväistalletuksesta. `Entities` sisältää käyttäjien ja piirrosten luokkia.

## Käyttöliittymä

On 3 päänäkymää, ja 1 ponnahdusikkuna:
- Kirjautumisnäkymä
- Menu näkymä
    - Uuden piirroksen tietojen näkymä
- Piirtonäkymä

Näissä 3 päänäkymässä on yhteiset piirteet joita siirsin `View` luokkaan. Ne myös käyttävät saman ikkunan, joten kerralla vain 1 voi olla aktiivinen ja `Ui` luokka on vastuussa niitten vaihdosta. 

Login näkymä on yksinkertaistettu, ei ole erillistä näkymää rekisteröinnin varten, vaan uusia käyttäjiä luodaan suoraan annetulla `user:pass` kombolla.

Menu näkymässä käyttäjä saa valita omista piirroksistaan tai luoda uutta.
Näkymä myös heittää ponnahdusikkunan johon syötetään uusien piirrosten nimi, leveys ja korkeus.

Piirtonäkymässä yritin matkia kunnon vanha `MS Pain`t; käyttäjä voi säätää laukevien komentojen välillä:

- suorakaide
- oval
- viiva
- teksti

Eka 3 komento pystyy värejäkin käsitellä, joita myös napeilla pystyy valita.

## Sovelluslogiikka

Sovelluksessa 1 [Käyttäjä](../src/entities/user.py) saa omistaa monta [Piirrosta](../src/entities/drawing.py):

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
    +Int id
    +Int width
    +Int height
    #List content

    +add(cmd, *args, **kwargs)
    +reproduce()
    +stringify()
}
```

Yritin eristää [Backend](../src/backend/backend.py) luokkaan sovelluksen niitä toimintoja joita en ois pystynyt järkevästi toteuttaa omissa pakkauksissaan.

Luokan ainoa olio hoitaa esim:
- kirjautumisen/rekisteröinnin
- kuvan tallentamisen, listaamisen, modaamisen

```mermaid
classDiagram
    Backend "1" --> "0-1" User
    User "1" --> "*" Drawing
```

## Pysyväistalletus

_Backend_ hallitsee tietokantaa taustalla, jossa 4 taulua:

- users
- drawings

- teachers
- templates

2 jälkimmäistä on jatkokehitystä miettien jo luotu valmiiksi. `CREATE TABLE IF NOT EXISTS` lauseiden ansiosta tietokantaa ei tarvitse erikseen rakentaa. Python:in kokonaisluvut tallennan `INTEGER`, Stringit `TEXT` muodossa. 
Olisi mennyt hirvee määrä resurssi keksiä ja normalisoida kaiken tarvitun taulun, joten piirrosten sisällön tallennus on varsin epätehokasta, JSON muodossa `TEXT`:ina. SQLite kuitenkin tukee myös json scalar funktioita, joten on myös mahdollista laajentaa sovellusta tässä muodossakin.
Tarkempaa tiedot kannan rakenteesta löydät Backend luokan [create_scheme](../src/backend/backend.py) methodista.

## Bonusyritys laittaa kasaan kaiken

Jätin sen kuitenkin kesken..

```mermaid
classDiagram
    View <|-- LoginView
    View <|-- MenuView
    View <|-- DrawingView
    
    Ui --|> Tk
    Ui --> LoginView
    Ui --> MenuView
    Ui --> DrawingView
    
    Backend <.. LoginView
    Backend <.. MenuView
    Backend <.. DrawingView

class User {
    +Int id
    +String name
    +Boolean teacher
}

class Drawing {
    +String name
    +Int id
    +Int width
    +Int height
    #List content

    +add(cmd, *args, **kwargs)
    +reproduce()
    +stringify()
}

class Backend {
    ~Int RECTANGLE
    ~Int OVAL
    ~Int LINE
    ~INT TEXT
    ~Exception WrongPassword

    #SQLite.Connection conn
    #User curr_user
    #Drawing curr_dwg
    #Int clicks
    #Int curr_cmd
    #String curr_fill
    #String curr_border
    #deque coords
    #tkinter.Canvas canvas

    #create_scheme()
    #draw(Int, *args, Boolean, **kwargs)
    
    +login_register()
    +get_curr_user()
    +get_user_dwgs()
    +save_curr_dwg()
    +get_curr_dwg()
    +set_curr_dwg(Drawing)
    +set_canvas(Canvas)
    +set_cmd(Int)
    +set_fill(String)
    +set_border(String)
    +b1_up(tkinter.Event)
    +b1_mv(tkinter.Event)
    +b1_dn(tkinter.Event)
    

}


class View {
    #master
    #frame
    #handle_prev
    #handle_next
    +destroy()
    +show()
}

class LoginView {
    #re_user
    #re_pass

    #create_widgets()
    #process_input()
}

class MenuView {
    #user

    #create_widgets()
    #proceed_to_next_view()
    #new_dwg(name, width, height)
}

class DrawingView {
    #User curr_user
    #Drawing curr_dwg
    #rows

    #create_widgets()
    #add_clr_btn(color)
    #undo()
    #redo()
    #save_and_exit()
}
```