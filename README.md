## PROGETTO CORSI UNIVERSITARI

Questo progetto riguarda lo sviluppo di un’applicazione web per la
gestione delle attività di orientamento (PCTO) del DAIS.
L’applicazione permetterà la creazione di nuovi corsi, ciascuno composto da
una o più lezioni tematiche da svolgersi in presenza oppure online.
Gli studenti potranno iscriversi e disiscriversi dai corsi, mentre i docenti
avranno accesso a un'interfaccia di analitica relativa ai corsi e potranno
inserire nuovi corsi o rimuoverne di esistenti, ed aggiungere lezioni ai corsi.
L’admin (il preside) potrà aggiungere un docente o rimuoverne uno esistente.

E’ stato utilizzato il DBMS ”sqlite” ed il livello di isolamento scelto è il
serializable, che garantisce che tutte le operazioni delle transazioni siano
eseguite come se ogni transazione occorresse una dopo l’altra in maniera
isolata.
