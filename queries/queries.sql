CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    pwd VARCHAR NOT NULL,
    UNIQUE(username)
);


CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INT NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    review VARCHAR NOT NULL
);

ALTER TABLE "reviews"
ADD "grade" integer NOT NULL;


INSERT INTO users (username, pwd) VALUES ('alexandrepernin', 'test');

UPDATE users
  SET pwd = 'XXX'
  WHERE username = 'alexandrepernin';

DELETE FROM users WHERE username = 'alexandrepernin';

SELECT * FROM users WHERE username = 'alexandrepernin' AND pwd = 'test';
