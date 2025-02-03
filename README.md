# BackEndTester

Elvis Starić

Fakultet informatike u Puli https://fipu.unipu.hr/

Kolegij: Raspodijeljeni sustavi - ntankovic.unipu.hr/rs

Mentor: doc. dr. sc. Nikola Tanković (ntankovic.unipu.hr)

BackEndTester je servis koji korisnicima omogućuje testiranje performansi backend-a njihove web aplikacije/servisa.

Funkcionalnosti:

1. Populacija baze podataka testnim podacima
2. Test backenda

## Populacija baze podataka

Ukoliko korisnik nema već popunjenu bazu podataka testnim podacima, isto je moguće napraviti kroz BackEndTester.
Korisnik unosi connection string na bazu te definira metapodatke - strukturu baze (relacije, primarni i strani ključevi,...).
Zatim je još potrebno priložiti .csv file u kojemu se nalaze podaci koji će se unijeti u bazu.

**Napomene**

- _Trenutno podržana samo MySQL baza podataka_
- _Imena atributa u .csv datoteci moraju biti isti onima u bazi_

## Test backenda

**Koraci**

1. Definicija parametara testa

   - Unos adrese backenda
   - Definicija broja korisnika za simulaciju
   - Definicija vremena trajanja testa
   - Definicija intervala ispisa rezultata

2. Definicija ruta za testiranje
   - Unos http metode (get, post, put, patch, delete)
   - Unos endpoint-a
   - Definicija payload-a _-opcionalno_

Nakon što su svi parametri definirani korisnik može pokrenuti izvršavanje testa. Po završetku izvršavanja korisnik dobiva rezultate testa u JSON formatu.

Rezultati testa sadrže timestamp (interval o kojemu se radi), broj obrađenih upita (throughput), te vrijeme najduže obrade upita u tom intervalu (maksimalna latencija).

_Primjer rezultata jednog intervala_

```
{
    "time": 10,
    "Responses:": 1000,
    "lat:": 20,
}
```
