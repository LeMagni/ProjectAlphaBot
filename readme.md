## Progetto TPSIT anno scolastico 2021-2022
# Alpha-BOBE

### TEAM:

Nome Alunno | Ruolo                                   
| - | - |
|Bongiovanni Daniele | Programmer / Designer
| Obertino Mattia | Game Designer


### TECNOLOGIE UTILIZZATE: 

Python, Flask, Raspberry, SQLite, AlphaBot

### DESCRIZIONE:

L'obiettivo di questo progetto era quello di riuscire a controllare un Alphabot tramite un sito web.
Per lo sviluppo di questo progetto abbiamo instaurato una connessione TCP client-server tramite l'utilizzo di Rapberry-PI e la libreria Flask che permette di creare un web-server.

<img src="IMG/schemaAb.png" align="center" width="800">

Nella prima pagina del sito bisogna loggarsi in modo che ogni comando che venga mandato sia salvato su un Database e sia riconducibile all'utente che l'ha effettuato.

<img src="https://github.com/BitMatt10111/PCTO-BulbsOff/blob/main/Logo%20e%20Immagini%20del%20Gioco/Icon.png" width="256">

Sul sito di controllo sono presenti i classici pulsanti di movimento (Avanti, Indietro, Destra, Sinistra) 
che tramite la connessione TCP inviasse al robot che movimento fare.
In un secondo momento abbiamo creato una seconda tabella sul DB in cui abbiamo inserito dei comandi composti
formati da una serie di movimenti semplici.


<img src="https://github.com/BitMatt10111/PCTO-BulbsOff/blob/main/Logo%20e%20Immagini%20del%20Gioco/Icon.png" width="256">
<img src="https://github.com/BitMatt10111/PCTO-BulbsOff/blob/main/Logo%20e%20Immagini%20del%20Gioco/Icon.png" width="256">
