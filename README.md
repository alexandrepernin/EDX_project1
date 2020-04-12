# Project 1

Book review website built using Python and FLASK. No ORM has been used in order to practice SQL.  
Users can:  
-Sign up, by providing a username and password.  
-Sign in, by providing their username and password.  
-Sign out from any page.  
-Search for information about a book. The search is done with the isbn number of the book, its title and/or the author's name. Information include average ratings from Goodreads as well as number of ratings.  
-Write reviews about a book, and consult reviews written by others on the website.  
-The route /api/<isbn> returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.  
