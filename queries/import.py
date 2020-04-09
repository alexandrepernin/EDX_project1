import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    books = pd.read_csv('books.csv', sep = ',')
    for row in range(len(books)):
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": books.isbn[row], "title": books.title[row], "author": books.author[row], "year":int(books.year[row])})
    db.commit()

if __name__ == "__main__":
    main()
