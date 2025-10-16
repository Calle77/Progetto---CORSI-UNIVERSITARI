CREATE TABLE User(
    id integer PRIMARY KEY AUTOINCREMENT,
    firstname varchar(100),
    lastname varchar(100),
    last_access varchar(100),
    email varchar(100) UNIQUE,
    password varchar(1000),
    is_admin Boolean DEFAULT false,
    is_docente Boolean DEFAULT false
);

CREATE TABLE Studenti_corso(
    cod_corso INTEGER,
    cod_user INTEGER,
    PRIMARY KEY(cod_corso, cod_user),
    FOREIGN KEY (cod_user) REFERENCES User(id),
    FOREIGN KEY (cod_corso) REFERENCES Corso(id) ON DELETE CASCADE
);

CREATE TABLE Corso(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome varchar(100),
    n_disponibili INTEGER DEFAULT 100,
    tipo varchar(100),
    id_docente integer,
    descrizione varchar(5000),
    FOREIGN KEY (id_docente) REFERENCES User(id) ON DELETE CASCADE
);


CREATE TABLE Lezione(
    nome varchar(100),
    data VARCHAR(100),
    fascia_oraria VARCHAR(100),
    cod_corso INTEGER,
    FOREIGN KEY (cod_corso) REFERENCES Corso(id) ON DELETE CASCADE,
    PRIMARY KEY (nome, cod_corso)
);



CREATE INDEX user_index ON User(id);
CREATE INDEX corso_index ON Corso(id);


CREATE TRIGGER iscrizioneCorso
    AFTER INSERT ON Studenti_corso
BEGIN
    UPDATE Corso
    SET n_disponibili = n_disponibili - 1
    WHERE id = NEW.cod_corso;
END;


CREATE TRIGGER disiscrizioneCorso
    AFTER DELETE ON Studenti_corso
BEGIN
    UPDATE Corso
    SET n_disponibili = n_disponibili + 1
    WHERE id = OLD.cod_corso;
END;


CREATE TRIGGER cancellaCorsi
    AFTER DELETE ON User
BEGIN
    DELETE FROM Corso 
    WHERE id_docente = OLD.id;
END;


