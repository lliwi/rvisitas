instructions = [
    'DROP TABLE IF EXISTS visitas;',
    'DROP TABLE IF EXISTS users;',
    """
        CREATE TABLE users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            user TEXT NOT NULL,
            password TEXT NOT NULL,
            creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """,
    """
        CREATE TABLE visitas (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            company TEXT NOT NULL,
            email TEXT NOT NULL,
            host TEXT NOT NULL,
            date DATETIME NOT NULL ,
            gdpr BOOLEAN NOT NULL
        );
    """,
    'INSERT INTO users (name, surname, user, password) values ("admin", "admin", "admin", "pbkdf2:sha256:260000$Jkd4rNsSI132MoDq$cff40255e53dbbea624e40eb8008bfaee5a318fcacbc6e4b0316a78f66cf9131");'



]
