# Project 1

Here is a book review website built using Python and FLASK. No ORM has been used in order to practice SQL.  
Users can:  
-Sign up, by providing a username and password.  
-Sign in, by providing their username and password.  
-Sign out from any page.  
-Search for information about a book. The search is done with the isbn number of the book, its title and/or the author's name. Information include average ratings from Goodreads (using Goodreads' API) as well as the number of ratings.  
-Write reviews about a book, and consult reviews written by others on the website.  
-The route /api/<isbn> returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average grade.  
Files:  
-application.py is the main Python file.  
-import.py is a program that takes the books contained in books.csv and import them into a PostgreSQL database. This database also contains a table for reviews (stores isbn, user id, grade and review) and one for users (stores username and password).  
-All html files are within the templates folder. All but one extend layout.html. Book.html extends layout_book.html (book page of the website). They all leverage Bootstrap4 and the styling defined in css/styles.css.  
-Queries.sql contains a bunch of sql queries that have been useful while building the website.
