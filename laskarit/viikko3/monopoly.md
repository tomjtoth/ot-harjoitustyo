```mermaid
classDiagram
    Lauta "1" --> "2-8" Pelaaja
    Lauta "1" --> "2" Noppa
    Lauta "1" <--> "40" Ruutu
    Pelaaja "1" --> "1" Nappula
    Nappula "1" --> "1" Ruutu
    class Ruutu {
        seuraava_ruutu
    }
```